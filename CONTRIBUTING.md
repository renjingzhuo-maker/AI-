# Contributing

Thanks for helping improve AI OSS Radar.

## Development Setup

```bash
cd ai-oss-radar
python -m pip install -e .
python -m unittest discover -s tests
```

## Pull Request Checklist

- Keep scoring changes explainable.
- Add or update tests for scoring behavior.
- Update `ai-oss-radar/docs/scoring.md` when weights or signals change.
- Prefer standard-library code unless a dependency clearly improves reliability.
