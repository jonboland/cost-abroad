import json

def food_costs():
    """Return required data from food JSON."""
    food = _get_food()
    food_cost = food["value"].values()
    country = list(food["dimension"]["geo"]["category"]["label"].values())
    country = _tidy_countries(country)
    return sorted(list(zip(country, food_cost)))

def _get_food():
    """Load food JSON."""
    with open('food_store.txt') as json_file:
        food = json.load(json_file)
    return food

def _tidy_countries(country):
    """Return updated country list."""
    country = ['Germany' if 'FRG' in x else x for x in country]
    country = ['Exclude' if 'Candidate' in x else x for x in country]
    return country
