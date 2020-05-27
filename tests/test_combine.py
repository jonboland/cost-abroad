import unittest
from unittest.mock import patch

import cost_abroad.combine


class CombineTests(unittest.TestCase):
    """Tests for the combine_cost_abroad module."""

    def setUp(self):
        self.cdata = [
            [["Malta", 77.8], ["Poland", 75.3]],
            [["Malta", 64.4], ["Poland", 69.1]],
            [["Malta", 50.2], ["Poland", 60.4]],
            [["Malta", 80.9], ["Poland", 49.3]],
            [["Malta", 62.1], ["Poland", 63.1]],
        ]

        self.combi = {
            "food": [["Malta", 77.8], ["Poland", 75.3]],
            "alcohol": [["Malta", 64.4], ["Poland", 69.1]],
            "transport": [["Malta", 50.2], ["Poland", 60.4]],
            "recreation": [["Malta", 80.9], ["Poland", 49.3]],
            "restaurant_hotel": [["Malta", 62.1], ["Poland", 63.1]],
            "overall": [("Malta", 67.1), ("Poland", 63.4)],
        }

    @patch("json.load", spec=True)
    @patch("builtins.open", spec=True)
    def test_create_combined_file_one_cat(self, mock_op, mock_js):
        """Test one price categories combined with overall."""
        mock_js.side_effect = [self.cdata[0]]
        result = cost_abroad.combine.create_combined_file(food="A010101")
        self.assertEqual(
            result,
            {
                "food": [["Malta", 77.8], ["Poland", 75.3]],
                "overall": [("Malta", 77.8), ("Poland", 75.3)],
            },
        )

    @patch("json.load", spec=True)
    @patch("builtins.open", spec=True)
    def test_create_combined_file_two_cats(self, mock_op, mock_js):
        """Test two price categories combined with overall."""
        mock_js.side_effect = self.cdata[0:2]
        result = cost_abroad.combine.create_combined_file(food="A010101", alcohol="A010201")
        self.assertEqual(
            result,
            {
                **{k: v for k, v in self.combi.items() if k in ("food", "alcohol")},
                **{"overall": [("Malta", 71.1), ("Poland", 72.2)]},
            },
        )

    @patch("json.load", spec=True)
    @patch("builtins.open", spec=True)
    def test_create_combined_file_all_cats(self, mock_op, mock_js):
        """Test all price categories combined with overall."""
        mock_js.side_effect = self.cdata
        result = cost_abroad.combine.create_combined_file(
            food="A010101",
            alcohol="A010201",
            transport="A0107",
            recreation="A0109",
            restaurant_hotel="A0111",
        )
        self.assertEqual(result, self.combi)

    @patch("builtins.open", spec=True)
    def test_combined_write_called_correctly(self, mock_op, spec=True):
        """Combined write called with correct file name."""
        path = cost_abroad.combine.Path(".\\data\\combined.txt")
        cost_abroad.combine.combined_write(
            {
                "food": [["Albania", 77.8], ["Bosnia and Herzegovina", 75.3]],
                "overall": [("Albania", 77.8), ("Bosnia and Herzegovina", 75.3)],
            }
        )
        open.assert_called_with(path, mode="w")


if __name__ == "__main__":
    unittest.main()

