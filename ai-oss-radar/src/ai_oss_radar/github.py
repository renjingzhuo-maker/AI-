from __future__ import annotations

import json
import os
from typing import Any
from urllib import error, parse, request

from .models import Repository


class GitHubClientError(RuntimeError):
    pass


class GitHubClient:
    def __init__(
        self,
        token: str | None = None,
        base_url: str = "https://api.github.com",
        timeout: int = 20,
    ) -> None:
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def search_repositories(
        self,
        query: str,
        limit: int = 25,
        sort: str = "stars",
        order: str = "desc",
    ) -> list[Repository]:
        if limit < 1:
            return []
        per_page = min(limit, 100)
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": str(per_page),
        }
        payload = self._get_json("/search/repositories", params=params)
        items = payload.get("items", [])[:limit]
        return [Repository.from_mapping(item) for item in items]

    def _get_json(self, path: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        if params:
            url = f"{url}?{parse.urlencode(params)}"

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "ai-oss-radar/0.1",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        req = request.Request(url, headers=headers)
        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code == 403:
                raise GitHubClientError(
                    "GitHub API rate limit or permission error. Set GITHUB_TOKEN and retry."
                ) from exc
            raise GitHubClientError(f"GitHub API error {exc.code}: {body}") from exc
        except error.URLError as exc:
            raise GitHubClientError(f"Network error: {exc.reason}") from exc


def build_ai_search_query(
    topic: str,
    min_stars: int = 100,
    pushed_after: str | None = None,
) -> str:
    terms = [f"topic:{topic}", f"stars:>={min_stars}", "archived:false"]
    if pushed_after:
        terms.append(f"pushed:>={pushed_after}")
    return " ".join(terms)
