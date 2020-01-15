import requests
import json

url = "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/prc_ppp_ind"

response = requests.get(
    url,
    headers={"Accept": "application/json"},
    params={
        "na_item": "PLI_EU28",
        "sinceTimePeriod": "2018",
        "groupedIndicators": "1",
        "precision": "1",
        "ppp_cat": ["A010101"],   #, "A0102"  
            }
    )

data = response.json()
print(json.dumps(data, sort_keys=False, indent=4))





