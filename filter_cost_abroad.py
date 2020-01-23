import json

# 'Germany (until 1990 former territory of the FRG) replaced with 'Germany'
countries = ['Albania', 'Austria', 'Bosnia and Herzegovina',
             'Belgium', 'Bulgaria', 'Estonia', 'Greece',
             'Spain', 'Switzerland', 'Cyprus', 'Czechia',
             'Germany', 'Denmark', '*EU - 28 countries',
             'Finland','France', 'Croatia', 'Hungary',
             'Ireland', 'Iceland', 'Italy', 'Lithuania',
             'Luxembourg', 'Latvia', 'Montenegro',
             'North Macedonia', 'Malta', 'Netherlands',
             'Norway','Poland', 'Portugal', 'Romania',
             'Serbia', 'Sweden', 'Slovenia', 'Slovakia',
             'Turkey', 'United Kingdom',
             ]

def food_costs():
    """Return required data from food JSON."""
    food = _get_food()
    food_cost = food["value"].values()
    country = list(food["dimension"]["geo"]["category"]["label"].values())
    country = _tidy_countries(country)
    return [x for x in sorted(list(zip(country, food_cost)))
              if x[0] in countries]

def _get_food():
    """Load food JSON."""
    with open('food_store.txt') as json_file:
        food = json.load(json_file)
    return food

def _tidy_countries(country):
    """Return updated country list."""
    # Hardcoding this will prob lead to errors with new datasets!
    del country[9]
    country.insert(9, 'Germany')
    del country[26]
    country.insert(26, '*EU - 28 countries')
    return country

print(food_costs())
