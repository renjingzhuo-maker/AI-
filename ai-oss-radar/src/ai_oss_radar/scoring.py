from __future__ import annotations

from datetime import UTC, datetime
import math

from .models import Repository, RepositoryScore, ScoredRepository


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def log_score(value: int, reference: int) -> float:
    if reference <= 0:
        raise ValueError("reference must be positive")
    return clamp(math.log1p(max(value, 0)) / math.log1p(reference))


def parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def recency_score(value: str | None, now: datetime, half_life_days: int) -> float:
    timestamp = parse_timestamp(value)
    if timestamp is None:
        return 0.0
    age_days = max((now - timestamp).total_seconds() / 86_400, 0)
    return clamp(0.5 ** (age_days / half_life_days))


def issue_health_score(open_issues: int, stars: int) -> float:
    if open_issues <= 0:
        return 1.0
    expected_open_issues = max(25, stars / 120)
    pressure = open_issues / expected_open_issues
    return clamp(1 - min(pressure, 2) * 0.35)


def score_repository(
    repository: Repository, now: datetime | None = None
) -> RepositoryScore:
    if now is None:
        now = datetime.now(tz=UTC)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=UTC)
    else:
        now = now.astimezone(UTC)

    usage = 100 * (
        log_score(repository.stars, 80_000) * 0.55
        + log_score(repository.forks, 20_000) * 0.25
        + log_score(repository.watchers, 30_000) * 0.20
    )

    fork_ratio = repository.forks / max(repository.stars, 1)
    ecosystem = 100 * (
        log_score(repository.stars, 120_000) * 0.25
        + clamp(fork_ratio / 0.22) * 0.20
        + clamp(len(repository.topics) / 8) * 0.20
        + (1.0 if repository.license_name else 0.0) * 0.15
        + (1.0 if repository.language else 0.0) * 0.10
        + (1.0 if repository.owner_type == "Organization" else 0.72) * 0.10
    )

    is_inactive = repository.archived or repository.disabled
    active_flag = 0.0 if is_inactive else 1.0
    fork_penalty = 0.82 if repository.is_fork else 1.0
    inactive_penalty = 0.65 if is_inactive else 1.0
    activity = 100 * (
        recency_score(repository.pushed_at, now, half_life_days=120) * 0.45
        + recency_score(repository.updated_at, now, half_life_days=180) * 0.25
        + active_flag * 0.20
        + issue_health_score(repository.open_issues, repository.stars) * 0.10
    )
    activity *= fork_penalty * inactive_penalty

    overall = usage * 0.35 + ecosystem * 0.35 + activity * 0.30
    reasons = build_reasons(repository, usage, ecosystem, activity)

    return RepositoryScore(
        usage=round(usage, 2),
        ecosystem=round(ecosystem, 2),
        activity=round(activity, 2),
        overall=round(overall, 2),
        reasons=tuple(reasons),
    )


def build_reasons(
    repository: Repository, usage: float, ecosystem: float, activity: float
) -> list[str]:
    reasons: list[str] = []
    if usage >= 72:
        reasons.append("strong adoption")
    elif usage >= 45:
        reasons.append("visible adoption")
    else:
        reasons.append("early adoption signal")

    if ecosystem >= 70:
        reasons.append("broad ecosystem relevance")
    elif repository.license_name and repository.topics:
        reasons.append("clear reuse signals")
    else:
        reasons.append("limited ecosystem metadata")

    if repository.archived or repository.disabled:
        reasons.append("maintenance risk")
    elif activity >= 70:
        reasons.append("recent maintenance activity")
    else:
        reasons.append("activity needs review")

    return reasons


def rank_repositories(
    repositories: list[Repository], now: datetime | None = None
) -> list[ScoredRepository]:
    scored = [
        ScoredRepository(repository=repository, score=score_repository(repository, now))
        for repository in repositories
    ]
    return sorted(scored, key=lambda item: item.score.overall, reverse=True)
