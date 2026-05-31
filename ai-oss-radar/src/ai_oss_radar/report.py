from __future__ import annotations

import json

from .models import ScoredRepository


def escape_markdown_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def to_markdown(
    scored_repositories: list[ScoredRepository],
    title: str = "AI OSS Radar",
) -> str:
    lines = [
        f"# {title}",
        "",
        "Repositories are scored on usage, ecosystem importance, and activity.",
        "",
        "| Rank | Repository | Overall | Usage | Ecosystem | Activity | Signals |",
        "| ---: | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for index, item in enumerate(scored_repositories, start=1):
        repo = item.repository
        score = item.score
        name = escape_markdown_table(repo.full_name)
        if repo.html_url:
            name = f"[{name}]({repo.html_url})"
        signals = escape_markdown_table(", ".join(score.reasons))
        lines.append(
            f"| {index} | {name} | {score.overall:.2f} | {score.usage:.2f} | "
            f"{score.ecosystem:.2f} | {score.activity:.2f} | {signals} |"
        )
    lines.append("")
    return "\n".join(lines)


def to_json(scored_repositories: list[ScoredRepository]) -> str:
    payload = []
    for item in scored_repositories:
        repo = item.repository
        score = item.score
        payload.append(
            {
                "repository": {
                    "full_name": repo.full_name,
                    "html_url": repo.html_url,
                    "stars": repo.stars,
                    "forks": repo.forks,
                    "watchers": repo.watchers,
                    "open_issues": repo.open_issues,
                    "topics": list(repo.topics),
                    "license_name": repo.license_name,
                    "language": repo.language,
                    "pushed_at": repo.pushed_at,
                    "updated_at": repo.updated_at,
                    "archived": repo.archived,
                    "disabled": repo.disabled,
                    "is_fork": repo.is_fork,
                    "owner_type": repo.owner_type,
                },
                "score": {
                    "usage": score.usage,
                    "ecosystem": score.ecosystem,
                    "activity": score.activity,
                    "overall": score.overall,
                    "reasons": list(score.reasons),
                },
            }
        )
    return json.dumps(payload, indent=2, ensure_ascii=False)
