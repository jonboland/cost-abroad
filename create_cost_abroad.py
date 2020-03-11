import json
import requests
from filter_cost_abroad import filter_prices


URL = 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/prc_ppp_ind'


def create_price_files():
    """Create price level data files for each category."""
    for name, value in categories.items():
        price_write(name, value[0])


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
        params={
            'na_item': 'PLI_EU28',
            'lastTimePeriod': '1',
            'precision': '1',
            'ppp_cat': code,
        }
    ).json()
    return prices


# Specified categories to include:
# (The overall category is automatically added prior to visualisation)
categories = {
    'food': ['A010101', 'magenta'],
    'alcohol': ['A010201', 'greens'],
    'transport': ['A0107', 'blues'],
    'recreation': ['A0109', 'purples'],
    'restaurant_hotel': ['A0111', 'teal'],
}

if __name__ == '__main__':
    create_price_files()
