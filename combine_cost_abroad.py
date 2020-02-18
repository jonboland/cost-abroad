import json


categories = (
    'food',
    'alcohol',
    'transport',
    'recreation',
    'restaurant_hotel',
    )

# Combine category values into a single dictionary.
def combined_values():
    cat_prices = {}
    for category in categories: 
        with open(f'{category}.txt') as json_file:
            prices = json.load(json_file)
        cat_prices[category] = prices
    return cat_prices
