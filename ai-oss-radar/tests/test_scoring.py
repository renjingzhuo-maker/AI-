from datetime import datetime, timezone
import unittest

from ai_oss_radar.models import Repository
from ai_oss_radar.scoring import rank_repositories, score_repository


NOW = datetime(2026, 5, 31, tzinfo=timezone.utc)


class ScoringTests(unittest.TestCase):
    def test_archived_repository_is_penalized_for_activity(self) -> None:
        repository = Repository(
            full_name="example/archived",
            stars=20_000,
            forks=4_000,
            watchers=20_000,
            topics=("ai", "llm"),
            license_name="MIT",
            language="Python",
            pushed_at="2026-05-20T00:00:00Z",
            updated_at="2026-05-20T00:00:00Z",
            archived=True,
            owner_type="Organization",
        )

        score = score_repository(repository, now=NOW)

        self.assertLess(score.activity, 80)
        self.assertIn("maintenance risk", score.reasons)

    def test_recent_project_can_rank_above_stale_project_with_similar_usage(self) -> None:
        active = Repository(
            full_name="example/active",
            stars=12_000,
            forks=2_300,
            watchers=12_000,
            topics=("ai", "rag", "llm", "agents"),
            license_name="Apache-2.0",
            language="Python",
            pushed_at="2026-05-20T00:00:00Z",
            updated_at="2026-05-22T00:00:00Z",
            owner_type="Organization",
        )
        stale = Repository(
            full_name="example/stale",
            stars=13_000,
            forks=2_100,
            watchers=13_000,
            topics=("ai", "rag"),
            license_name="Apache-2.0",
            language="Python",
            pushed_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
            owner_type="Organization",
        )

        ranked = rank_repositories([stale, active], now=NOW)

        self.assertEqual(ranked[0].repository.full_name, "example/active")

    def test_mapping_accepts_github_api_shape(self) -> None:
        repository = Repository.from_mapping(
            {
                "full_name": "org/project",
                "stargazers_count": 100,
                "forks_count": 20,
                "watchers_count": 100,
                "open_issues_count": 3,
                "topics": ["ai", "llm"],
                "license": {"spdx_id": "MIT"},
                "owner": {"type": "Organization"},
            }
        )

        self.assertEqual(repository.stars, 100)
        self.assertEqual(repository.license_name, "MIT")
        self.assertEqual(repository.owner_type, "Organization")


if __name__ == "__main__":
    unittest.main()
