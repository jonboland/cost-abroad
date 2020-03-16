"""
Request JSON from eurostat server for cost categories
and write filtered price data to a local JSON file for each.

One or more of the below keyword arguments must be passed
to the create_price_files function:

food='A010101'
alcohol='A010201'
transport='A0107'
recreation='A0109'
restaurant_hotel='A0111'
"""


import json
import requests
from filter_cost_abroad import filter_prices


URL = 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/prc_ppp_ind'


def create_price_files(**kwargs):
    """Create price level data files for each category."""
    for name, value in kwargs.items():
        price_write(name, value)


def price_write(name, code):
    """Write raw price data for a category to local file."""
    prices = price_raw(code)
    filtered_prices = filter_prices(prices)
    with open(f'{name}.txt', 'w') as outfile:
        json.dump(filtered_prices, outfile)


def price_raw(code):
    """Request JSON from eurostat server for a category."""
    prices = requests.get(
        URL,
        headers={'Accept': 'application/json'},
        params={'na_item': 'PLI_EU28',
                'lastTimePeriod': '1',
                'precision': '1',
                'ppp_cat': code,
        }
    ).json()
    return prices
