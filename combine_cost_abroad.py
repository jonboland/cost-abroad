"""
Combine JSON cost category data from local files into a single JSON
file and add an overall category.

One or more of the below keyword arguments must be passed
to the create_combined_file function:

food='A010101'
alcohol='A010201'
transport='A0107'
recreation='A0109'
restaurant_hotel='A0111'

An individual file for each passed category must be present
or a FileNotFoundError will be generated.
"""


import json
from statistics import mean
from collections import defaultdict


def create_combined_file(**kwargs):
    """Combine category values into a single file with overall category."""
    cat_prices = {}
    for category in kwargs:
        with open(f'{category}.txt') as json_file:
            prices = json.load(json_file)
        cat_prices[category] = prices
    cat_prices['overall'] = _add_overall(cat_prices)
    combined_write(cat_prices)
    return cat_prices


def combined_write(cat_prices):
    """Write combined values data to local file."""
    with open('combined.txt', 'w') as outfile:
        json.dump(cat_prices, outfile)


def _add_overall(cat_prices):
    """Create overall category to add to combined prices dictionary."""
    grouped = defaultdict(list)
    for item in cat_prices.values():
        for country, price in item:
            grouped[country].append(price)
    average = {k:round(mean(v), 1) for k,v in grouped.items()}
    return list(average.items())
