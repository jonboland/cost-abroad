"""
Request JSON from eurostat server for cost categories
and write filtered price data to a local JSON file for each.

One or more of the below keyword arguments must be passed
to the create_price_files function:

food='A010101'
alcohol='A010201'
transport='A0107'
recreation='A0109'
restaurant_hotel='A0111'
"""


import json
import requests
from filter_cost_abroad import filter_prices


URL = "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/prc_ppp_ind"


def create_price_files(**kwargs):
    """Create price level data files for each category."""
    for name, code in kwargs.items():
        create_price_file(name, code)


def create_price_file(name, code):
    """Create price level data file for a category."""
    prices = prices_raw(code)
    filtered_prices = filter_prices(prices)
    write_prices(name, filtered_prices)
    return filtered_prices


def write_prices(name, filtered_prices):
    with open(f"{name}.txt", "w") as outfile:
        json.dump(filtered_prices, outfile)


def prices_raw(code):
    try:
        response = requests.get(
            URL,
            headers={"Accept": "application/json"},
            params={
                "na_item": "PLI_EU28",
                "lastTimePeriod": "1",
                "precision": "1",
                "ppp_cat": code,
            },
        )
        if "Dataset contains no data" in response.text:
            print("invalid category reference number provided")
        elif not response.text:
            print("there was a problem handling your request")
        else:
            return response.json()
    except requests.ConnectionError:
        print("failed to connect")
    else:
        if not 200 <= response.status_code <= 299:
            print(f"status code: {response.status_code} outside of 2xx range")