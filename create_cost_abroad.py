import json
import requests

url = "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/prc_ppp_ind"

food = requests.get(
    url,
    headers={"Accept": "application/json"},
    params={
        "na_item": "PLI_EU28",
        "sinceTimePeriod": "2018",
        "groupedIndicators": "1",
        "precision": "1",
        "ppp_cat": ["A010101"],   #, "A0102"  
            }
    ).json()

with open('food_store.txt', 'w') as outfile:
    json.dump(food, outfile)



