import unittest

from ai_oss_radar.models import Repository
from ai_oss_radar.report import to_markdown
from ai_oss_radar.scoring import rank_repositories


class ReportTests(unittest.TestCase):
    def test_markdown_report_contains_scores_and_links(self) -> None:
        repository = Repository(
            full_name="org/ai-tool",
            html_url="https://github.com/org/ai-tool",
            stars=1000,
            forks=120,
            watchers=1000,
            topics=("ai", "llm"),
            license_name="MIT",
            language="Python",
            pushed_at="2026-05-20T00:00:00Z",
            updated_at="2026-05-20T00:00:00Z",
            owner_type="Organization",
        )

        report = to_markdown(rank_repositories([repository]), title="Test Radar")

        self.assertIn("# Test Radar", report)
        self.assertIn("[org/ai-tool](https://github.com/org/ai-tool)", report)
        self.assertIn("| Rank | Repository | Overall |", report)


if __name__ == "__main__":
    unittest.main()
