from io import StringIO
import unittest
from unittest.mock import patch, call

import responses

import cost_abroad.create


URL = "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/prc_ppp_ind"


class CreateTests(unittest.TestCase):
    """Tests for the create module."""

    @patch("cost_abroad.create.create_price_file", spec=True)
    def test_create_price_files(self, mock_cpf):
        """Call create price file with two differnt categories."""
        cost_abroad.create.create_price_files(alcohol="A010201", transport="A0107")
        self.assertEqual(
            mock_cpf.mock_calls,
            [call("alcohol", "A010201"), call("transport", "A0107")],
        )

    @patch("cost_abroad.create.write_prices", spec=True)
    @patch(
        "cost_abroad.create.prices_raw",
        spec=True,
        return_value={
            "value": {"0": 77.8},
            "dimension": {
                "geo": {"category": {"index": {"AL": 0}, "label": {"AL": "Albania"}}}
            },
        },
    )
    def test_create_price_file(self, mock_pr, mock_wp):
        """Create price file returns list containing a tuple."""
        result = cost_abroad.create.create_price_file("food", "A010101")
        self.assertEqual(result, [("Albania", 77.8)])

    @patch("builtins.open")
    def test_write_prices_called_correctly(self, mock_op):
        """Write prices files called with correct category file name."""
        # path = cost_abroad.create.Path(".\\data\\recreation.txt")
        path = cost_abroad.create.Path(__file__).resolve().parent.parent / "data" / "recreation.txt"
        cost_abroad.create.write_prices("recreation", [("Germany", 103.2)])
        open.assert_called_with(path, mode="w")

    @patch("cost_abroad.create.requests.get", spec=True)
    def test_get_is_called_correctly(self, get_js):
        """Get is called with correct URL and parameters."""
        cost_abroad.create.prices_raw("A0109")
        get_js.assert_called_with(
            URL,
            headers={"Accept": "application/json"},
            params={
                "na_item": "PLI_EU28",
                "lastTimePeriod": "1",
                "precision": "1",
                "ppp_cat": "A0109",
            },
        )

    @patch("cost_abroad.create.requests.get")
    def test_connection_error_suppressed(self, mock_get):
        """Default error text suppressed if connection error encountered."""
        mock_get.side_effect = cost_abroad.create.requests.exceptions.ConnectionError()
        self.assertIsNone(cost_abroad.create.prices_raw("A0111"))

    @responses.activate
    def test_correct_message_printed_if_no_data_in_response(self):
        """Correct console message printed if eurostat returns empty dataset."""
        responses.add(
            responses.GET, URL, body='{"error": "Dataset contains no data"}', status=400
        )
        with patch("sys.stdout", new=StringIO()) as mock_out:
            cost_abroad.create.prices_raw("invalidcodetest")
        self.assertIn("invalid category", mock_out.getvalue())

    @responses.activate
    def test_correct_message_printed_if_server_error(self):
        """Correct console message printed if server error returned."""
        responses.add(responses.GET, URL, status=500)
        with patch("sys.stdout", new=StringIO()) as mock_out:
            cost_abroad.create.prices_raw("A010101")
        self.assertIn("500 outside", mock_out.getvalue())

    @responses.activate
    def test_json_returned_if_valid_code_provided(self):
        """JSON is returned if valid price category given as argument."""
        responses.add(responses.GET, URL, body=r'{"value": {"0": 77}}')
        result = cost_abroad.create.prices_raw("A010201")
        self.assertEqual(result, {"value": {"0": 77}})


if __name__ == "__main__":
    unittest.main()
