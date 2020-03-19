import unittest
from unittest.mock import patch, call
import create_cost_abroad
from io import StringIO
import responses



URL = 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/prc_ppp_ind'



class CreateTests(unittest.TestCase):
    """Tests for the create_cost_abroad module."""

    @patch('create_cost_abroad.create_price_file', spec=True)
    def test_create_price_files(self, mock_create_price_file):
        """Call create price file with two differnt categories."""
        create_cost_abroad.create_price_files(alcohol='A010201',
                                              transport='A0107')
        self.assertEqual(mock_create_price_file.mock_calls,
                         [call('alcohol', 'A010201'),
                          call('transport', 'A0107')])


    @patch('create_cost_abroad.write_prices', spec=True)
    @patch('create_cost_abroad.prices_raw', spec=True,
           return_value={"value": {"0": 77.8}, "dimension": {"geo": {"category":
                        {"index": {"AL": 0}, "label": {"AL": "Albania"}}}}})
    def test_create_price_file(self, mock_prices_raw, mock_write_prices):
        """Create price file returns list containing a tuple."""
        result = create_cost_abroad.create_price_file('food', 'A010101')
        self.assertEqual(result, [('Albania', 77.8)])


    @patch('builtins.open')
    def test_write_prices_called_correctly(self, mock_op):
        """Write prices files called with correct category file name."""
        create_cost_abroad.write_prices('food', [('Albania', 77.8)])
        open.assert_called_with('food.txt', 'w')


    @patch('create_cost_abroad.requests.get', spec=True)
    def test_get_is_called_correctly(self, get_json):
        """Get is called with correct URL and parameters."""
        create_cost_abroad.prices_raw('A010101')
        get_json.assert_called_with(URL,
                                    headers={'Accept': 'application/json'},
                                    params={'na_item': 'PLI_EU28',
                                            'lastTimePeriod': '1',
                                            'precision': '1',
                                            'ppp_cat': 'A010101',
                                            }
                                    )


    @patch('create_cost_abroad.requests.get')
    def test_connection_error_suppressed(self, mock_get):
        """Default error text suppressed if connection error encountered."""
        mock_get.side_effect = (create_cost_abroad.requests.
                                exceptions.ConnectionError())
        self.assertIsNone(create_cost_abroad.prices_raw('A010101'))


    @responses.activate
    def test_correct_message_printed_if_no_data_in_response(self):
        """Correct console message printed if eurostat returns empty dataset."""
        responses.add(responses.GET, URL,
                      body='{"error": "Dataset contains no data"}', status=400)
        with patch('sys.stdout', new=StringIO()) as mock_out:
            create_cost_abroad.prices_raw('invalidcodetest')
        self.assertIn('invalid category', mock_out.getvalue())


    @responses.activate
    def test_correct_message_printed_if_server_error(self):
        """Correct console message printed if server error returned."""
        responses.add(responses.GET, URL, status=500)
        with patch('sys.stdout', new=StringIO()) as mock_out:
            create_cost_abroad.prices_raw('A010101')
        self.assertIn('500 outside', mock_out.getvalue())


    @responses.activate
    def test_json_returned_if_valid_code_provided(self):
        """JSON is returned if valid price category given as argument."""
        responses.add(responses.GET, URL, body=r'{"value": {"0": 77}}')
        result = create_cost_abroad.prices_raw('A010101')
        self.assertEqual(result, {"value": {"0": 77}})



if __name__ == '__main__':
        unittest.main()
