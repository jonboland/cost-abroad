import json
from statistics import mean
from collections import defaultdict
from create_cost_abroad import categories


def combined_values():
    """Combine category values into a single file with overall category."""
    cat_prices = {}
    for category in categories:
        with open(f'{category}.txt') as json_file:
            prices = json.load(json_file)
        cat_prices[category] = prices
    cat_prices['overall'] = _add_overall(cat_prices)
    _combined_write(cat_prices)


def _combined_write(cat_prices):
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


if __name__ == '__main__':
    combined_values()
