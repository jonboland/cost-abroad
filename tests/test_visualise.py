import unittest

from snapshot_test import DashSnapshotTestCase

import context
import visualise


class VisualiseTests(DashSnapshotTestCase):
    """Tests for the visualise module."""

    def test_html_snapshot_matches_reference(self):
        """Test Dash app html snapshot matches reference snapshot."""
        my_component = visualise.app.layout
        # Increment id to recreate snapshot when running test
        self.assertSnapshotEqual(my_component, "id-009")

    def test_choropleth_contains_country_list_excerpt(self):
        """Test update_figure passing country list entries to choropleth."""
        # Excerpt includes entries dependent on filter's tidy function
        excerpt = (
            '"Exclude", "Finland", "France", "Germany", '
            '"Greece", "Hungary", "Iceland", "Ireland", "Italy", '
            '"Latvia", "Lithuania", "Luxembourg", "Malta", '
            '"Montenegro", "Netherlands", "North Macedonia", '
            '"Norway", "Poland", "Portugal", "Romania", "Serbia", '
            '"Slovakia", "Slovenia", "Spain", "Sweden", '
            '"Switzerland", "Turkey", "United Kingdom"'
        )
        result = visualise.update_figure("overall")
        self.assertIn(excerpt, result)


if __name__ == "__main__":
    unittest.main()
