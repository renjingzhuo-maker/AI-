# AI OSS Radar

AI OSS Radar ranks AI-related GitHub repositories by three signals that matter when choosing projects to depend on, contribute to, or study:

- **Usage**: stars, forks, and watchers.
- **Ecosystem importance**: reuse signals such as forks, topics, license, language, and organization ownership.
- **Activity**: recent pushes, recent updates, archive status, and issue pressure.

The project is intentionally small: it uses the Python standard library, works as a CLI, and can also be imported as a library.

## Why This Project

AI tooling changes quickly. A repository with many stars but no recent maintenance can be risky, while an active project with clear reuse signals may be a better long-term bet. AI OSS Radar gives teams a repeatable first-pass score before they do deeper technical review.

## Quick Start

```bash
python -m ai_oss_radar score --input examples/seed_repositories.json
```

Write a Markdown report:

```bash
python -m ai_oss_radar score \
  --input examples/seed_repositories.json \
  --output reports/ai-radar.md
```

Discover live GitHub repositories:

```bash
GITHUB_TOKEN=ghp_your_token_here python -m ai_oss_radar discover \
  --topic llm \
  --min-stars 1000 \
  --pushed-after 2025-01-01 \
  --limit 25 \
  --output reports/llm-radar.md
```

`GITHUB_TOKEN` is optional, but recommended because unauthenticated GitHub API requests are rate-limited.

## Example Output

| Rank | Repository | Overall | Usage | Ecosystem | Activity | Signals |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | huggingface/transformers | 94.73 | 100.00 | 93.18 | 90.40 | strong adoption, broad ecosystem relevance, recent maintenance activity |
| 2 | langchain-ai/langchain | 93.99 | 99.73 | 89.46 | 92.56 | strong adoption, broad ecosystem relevance, recent maintenance activity |

## Scoring Philosophy

The score is not a replacement for a technical audit. It is a practical triage tool:

- High usage means many people have found the project useful.
- High ecosystem score means the project is easier to reuse and more likely to matter beyond a single demo.
- High activity means the repository looks maintained recently.

Read [docs/scoring.md](docs/scoring.md) for details.

## Library Usage

```python
from ai_oss_radar import Repository, rank_repositories

repositories = [
    Repository(
        full_name="example/ai-project",
        stars=1200,
        forks=180,
        watchers=1200,
        topics=("ai", "llm"),
        license_name="MIT",
        language="Python",
        pushed_at="2026-05-20T00:00:00Z",
        updated_at="2026-05-22T00:00:00Z",
        owner_type="Organization",
    )
]

print(rank_repositories(repositories)[0].score.overall)
```

## Development

```bash
python -m unittest discover -s tests
```

Optional editable install:

```bash
python -m pip install -e .
```

## Roadmap

- Add repository release cadence scoring.
- Add contributor diversity scoring.
- Add dependency ecosystem enrichment for Python, JavaScript, and Rust packages.
- Add optional LLM-generated repository summaries.
- Publish scheduled benchmark reports for AI topics such as `llm`, `rag`, `agents`, and `computer-vision`.

## License

MIT
