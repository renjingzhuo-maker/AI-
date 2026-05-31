# Contributing

Thanks for helping improve AI OSS Radar.

## Development Setup

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

## Pull Request Checklist

- Keep scoring changes explainable.
- Add or update tests for scoring behavior.
- Update `docs/scoring.md` when weights or signals change.
- Prefer standard-library code unless a dependency clearly improves reliability.

## Good First Issues

- Add more sample repository fixtures.
- Improve Markdown report formatting.
- Add CSV export.
- Add topic presets for common AI domains.
