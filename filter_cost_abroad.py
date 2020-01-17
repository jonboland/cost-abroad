import json

with open('food_store.txt') as json_file:
    food = json.load(json_file)

countries = ['Albania', 'Austria', 'Bosnia and Herzegovina',
             'Belgium', 'Bulgaria', 'Estonia', 'Greece', 'Spain', 'Switzerland', 'Cyprus',
             'Czechia', 'Germany (until 1990 former territory of the FRG)',
             'Denmark', 'European Union - 28 countries', 'Finland',
             'France', 'Croatia', 'Hungary', 'Ireland', 'Iceland',
             'Italy', 'Lithuania', 'Luxembourg', 'Latvia', 'Montenegro',
             'North Macedonia', 'Malta', 'Netherlands', 'Norway',
             'Poland', 'Portugal', 'Romania', 'Serbia', 'Sweden',
             'Slovenia', 'Slovakia', 'Turkey', 'United Kingdom',
             'Kosovo (under United Nations Security Council Resolution 1244/99)',
             ]

def food_ratios(raw_data):
    food_cost = food["value"].values()
    country = list(food["dimension"]["geo"]["category"]["label"].values())
    zipped = sorted(list(zip(country, food_cost)))
    return zipped


print(food_ratios(food))
