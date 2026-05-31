from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Repository:
    """Normalized repository signals used by the scoring engine."""

    full_name: str
    description: str = ""
    html_url: str = ""
    stars: int = 0
    forks: int = 0
    watchers: int = 0
    open_issues: int = 0
    topics: tuple[str, ...] = field(default_factory=tuple)
    license_name: str | None = None
    language: str | None = None
    pushed_at: str | None = None
    updated_at: str | None = None
    archived: bool = False
    disabled: bool = False
    is_fork: bool = False
    owner_type: str | None = None

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "Repository":
        license_value = data.get("license")
        if isinstance(license_value, dict):
            license_name = license_value.get("spdx_id") or license_value.get("name")
        else:
            license_name = data.get("license_name") or license_value

        owner_value = data.get("owner")
        owner_type = data.get("owner_type")
        if isinstance(owner_value, dict):
            owner_type = owner_type or owner_value.get("type")

        topics = data.get("topics") or ()
        if isinstance(topics, str):
            topics = tuple(topic.strip() for topic in topics.split(",") if topic.strip())

        return cls(
            full_name=str(data.get("full_name") or data.get("name") or ""),
            description=str(data.get("description") or ""),
            html_url=str(data.get("html_url") or data.get("url") or ""),
            stars=int(data.get("stargazers_count", data.get("stars", 0)) or 0),
            forks=int(data.get("forks_count", data.get("forks", 0)) or 0),
            watchers=int(data.get("watchers_count", data.get("watchers", 0)) or 0),
            open_issues=int(
                data.get("open_issues_count", data.get("open_issues", 0)) or 0
            ),
            topics=tuple(str(topic).lower() for topic in topics),
            license_name=license_name,
            language=data.get("language"),
            pushed_at=data.get("pushed_at"),
            updated_at=data.get("updated_at"),
            archived=bool(data.get("archived", False)),
            disabled=bool(data.get("disabled", False)),
            is_fork=bool(data.get("fork", data.get("is_fork", False))),
            owner_type=owner_type,
        )


@dataclass(frozen=True)
class RepositoryScore:
    usage: float
    ecosystem: float
    activity: float
    overall: float
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class ScoredRepository:
    repository: Repository
    score: RepositoryScore
