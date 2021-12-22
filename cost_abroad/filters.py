"""
Take raw JSON received from eurostat server for a cost category
and return filtered price data with tidied country names.
"""


def filter_prices(prices):
    """Filter price file to leave required data."""
    category_cost = prices["value"].values()
    countries = list(prices["dimension"]["geo"]["category"]["label"].values())
    countries = _tidy_countries(countries)
    return sorted(list(zip(countries, category_cost)))


def _tidy_countries(countries):
    """
    Return country list with some names tidied or excluded 
    so names and values match up and display correctly on the choropleth.
    """
    return [
        # The name given to Germany needs to be shortened because it's much too long
        "Germany" if "FRG" in name
        # The candidate country text includes the word Turkey,
        # which would be picked up and displayed incorrectly on the map
        else "Exclude" if "Candidate" in name
        else name for name in countries
        # The EU 28 entry is missing from the values list,
        # so it must be ignored to avoid a misalignment between names and values
        if "28" not in name
    ]
