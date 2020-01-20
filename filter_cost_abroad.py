import json

countries = ['Albania', 'Austria', 'Bosnia and Herzegovina',
             'Belgium', 'Bulgaria', 'Estonia', 'Greece',
             'Spain', 'Switzerland', 'Cyprus', 'Czechia',
             'Germany (until 1990 former territory of the FRG)',
             'Denmark', 'European Union - 28 countries',
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
    country = food["dimension"]["geo"]["category"]["label"].values()
    return [x for x in sorted(list(zip(country, food_cost)))
              if x[0] in countries]

def _get_food():
    """Load food JSON."""
    with open('food_store.txt') as json_file:
        food = json.load(json_file)
    return food

print(food_costs())

