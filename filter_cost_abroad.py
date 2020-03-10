
def filter_prices(prices):
    """Filter price file to leave required data."""
    category_cost = prices["value"].values()
    countries = list(prices["dimension"]["geo"]["category"]["label"].values())
    countries = _tidy_countries(countries)
    return sorted(list(zip(countries, category_cost)))


def _tidy_countries(countries):
    """Return updated country list."""
    tidy = ['Germany' if 'FRG' in x else x for x in countries]
    # Without this Turkey is listed as candidate
    tidy = ['Exclude' if 'Candidate' in x else x for x in tidy]
    return tidy
