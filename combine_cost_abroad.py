import json
from statistics import mean


categories = ('food', 'alcohol', 'transport',
              'recreation', 'restaurant_hotel')


def combined_values():
    """Combine category values into single dict with overall cat."""
    cat_prices = {}
    for category in categories:
        with open(f'{category}.txt') as json_file:
            prices = json.load(json_file)
        cat_prices[category] = prices
    cat_prices['overall'] = _add_overall(cat_prices)
    return cat_prices


def _add_overall(cat_prices):
    """Create overall category to add to combined prices dictionary."""
    # Create nested list and insert country names
    overall = [[x[0], []] for x in cat_prices[categories[0]]]
    # Add stats for each selected category to the relevant country
    for cat_stats in cat_prices.values():
        for country_stat in cat_stats:
            for combined_stats in overall:
                if combined_stats[0] == country_stat[0]:
                    combined_stats[1].append(country_stat[1])
    # Replace stats with average for each country
    for combined_stats in overall:
        combined_stats[1] = round(mean(combined_stats[1]), 1)
    return overall
