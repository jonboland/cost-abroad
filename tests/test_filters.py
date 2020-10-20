import unittest

import context
import filters


class FiltersTests(unittest.TestCase):
    """Tests for the filters module."""

    def test_filter_no_tidy(self):
        """List of tuples containing name and value should be returned."""
        snip = {
            "label": "Purchasing power parities (PPPs)",
            "source": "Eurostat",
            "class": "dataset",
            "value": {"0": 77.8, "1": 126.6, "2": 75.3},
            "dimension": {
                "geo": {
                    "category": {
                        "index": {"AL": 0, "AT": 1, "BA": 2},
                        "label": {
                            "AL": "Albania",
                            "AT": "Austria",
                            "BA": "Bosnia and Herzegovina",
                        },
                    }
                }
            },
        }

        filtered = filters.filter_prices(snip)
        self.assertEqual(
            filtered,
            [("Albania", 77.8), ("Austria", 126.6), ("Bosnia and Herzegovina", 75.3)],
        )

    def test_filter_tidy_frg(self):
        """FRG should be replaced with Germany via tidy_countries."""
        snip = {
            "value": {"0": 77.8, "1": 126.6, "2": 102.4},
            "dimension": {
                "geo": {
                    "category": {
                        "index": {"AL": 0, "AT": 1, "DE": 2},
                        "label": {
                            "AL": "Albania",
                            "AT": "Austria",
                            "DE": "Germany (until 1990 former territory of the FRG)",
                        },
                    }
                }
            },
        }

        tdy_frg = filters.filter_prices(snip)
        self.assertEqual(
            tdy_frg, [("Albania", 77.8), ("Austria", 126.6), ("Germany", 102.4)]
        )

    def test_filter_tidy_candidate(self):
        """Candidate should be replaced with Exclude via tidy_countries."""
        snip = {
            "value": {"0": 77.8, "1": 75.3, "2": 74.4},
            "dimension": {
                "geo": {
                    "category": {
                        "index": {"AL": 0, "BA": 1, "CPC1": 2},
                        "label": {
                            "AL": "Albania",
                            "BA": "Bosnia and Herzegovina",
                            "CPC1": "Candidate and potential candidate countries "
                            "except Turkey and Kosovo (under United Nations "
                            "Security Council Resolution 1244/99)",
                        },
                    }
                }
            },
        }

        tdy_can = filters.filter_prices(snip)
        self.assertEqual(
            tdy_can,
            [("Albania", 77.8), ("Bosnia and Herzegovina", 75.3), ("Exclude", 74.4)],
        )


if __name__ == "__main__":
    unittest.main()
