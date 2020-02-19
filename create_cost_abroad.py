import json
import requests
from filter_cost_abroad import filter_prices


url = 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/prc_ppp_ind'


def create_price_files():
    """Create price level data files for each category."""
    categories = {
        'food': 'A010101',
        'alcohol': 'A010201',
        'transport': 'A0107',
        'recreation': 'A0109',
        'restaurant_hotel': 'A0111',
    }
    for name, code in categories.items():
        price_write(f'{name}', f'{code}')


def price_write(name, code):
    """Write raw price data for a category to local file."""
    prices = price_raw(code)
    prices = filter_prices(prices)
    with open(f'{name}.txt', 'w') as outfile:
        json.dump(prices, outfile)


def price_raw(code):
    """Request JSON from eurostat web server."""
    prices = requests.get(
        url,
        headers={'Accept': 'application/json'},
        params={
            'na_item': 'PLI_EU28',
            'lastTimePeriod': '1',
            'precision': '1',
            'ppp_cat': code,
        },
    ).json()
    return prices

create_price_files()
