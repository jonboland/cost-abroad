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
    """Return updated country list."""
    return [
        "Germany" if "FRG" in name
        else name for name in countries
        if "28" not in name
    ]
