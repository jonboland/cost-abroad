import unittest
from unittest.mock import patch

import context
import run


class RunTest(unittest.TestCase):
    """Test for the run_files module."""

    @patch("run.create_price_files", spec=True)
    @patch("run.create_combined_file", spec=True)
    def test_create_and_combined_called_correctly(self, mock_cf, mock_pf):
        """Test category file and combined file functions called correctly."""
        run.main()
        run.create_price_files.assert_called_with(
            food="A010101",
            alcohol="A010201",
            transport="A0107",
            recreation="A0109",
            restaurant_hotel="A0111",
        )
        run.create_combined_file.assert_called_with(
            food="A010101",
            alcohol="A010201",
            transport="A0107",
            recreation="A0109",
            restaurant_hotel="A0111",
        )


if __name__ == "__main__":
    unittest.main()

