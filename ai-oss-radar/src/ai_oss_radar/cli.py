from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .github import GitHubClient, GitHubClientError, build_ai_search_query
from .models import Repository
from .report import to_json, to_markdown
from .scoring import rank_repositories


def load_repositories(path: Path) -> list[Repository]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, dict):
        payload = payload.get("items", payload.get("repositories", []))
    if not isinstance(payload, list):
        raise ValueError("input JSON must contain a list of repositories")
    return [Repository.from_mapping(item) for item in payload]


def render(scored: list, output_format: str, title: str) -> str:
    if output_format == "json":
        return to_json(scored)
    return to_markdown(scored, title=title)


def write_or_print(content: str, output: Path | None) -> None:
    if output is None:
        print(content)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")


def add_score_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "score", help="Score repositories from a local GitHub-style JSON file."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--title", default="AI OSS Radar")
    parser.set_defaults(handler=handle_score)


def add_discover_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "discover", help="Search GitHub for AI repositories and rank the results."
    )
    parser.add_argument("--topic", default="llm")
    parser.add_argument("--min-stars", type=int, default=1000)
    parser.add_argument("--pushed-after", help="Date filter such as 2025-01-01.")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--title", default="AI OSS Radar")
    parser.set_defaults(handler=handle_discover)


def handle_score(args: argparse.Namespace) -> int:
    repositories = load_repositories(args.input)
    scored = rank_repositories(repositories)
    write_or_print(render(scored, args.format, args.title), args.output)
    return 0


def handle_discover(args: argparse.Namespace) -> int:
    query = build_ai_search_query(
        topic=args.topic,
        min_stars=args.min_stars,
        pushed_after=args.pushed_after,
    )
    client = GitHubClient()
    try:
        repositories = client.search_repositories(query=query, limit=args.limit)
    except GitHubClientError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    scored = rank_repositories(repositories)
    write_or_print(render(scored, args.format, args.title), args.output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-oss-radar",
        description="Rank AI GitHub repositories by adoption, ecosystem importance, and activity.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_score_parser(subparsers)
    add_discover_parser(subparsers)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)
