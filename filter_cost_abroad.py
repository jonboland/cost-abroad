
def filter_prices(prices):
    """Filter price file to leave required data."""
    category_cost = prices["value"].values()
    country = list(prices["dimension"]["geo"]["category"]["label"].values())
    country = _tidy_countries(country)
    return sorted(list(zip(country, category_cost)))

def _tidy_countries(country):
    """Return updated country list."""
    country = ['Germany' if 'FRG' in x else x for x in country]
    country = ['Exclude' if 'Candidate' in x else x for x in country]
    return country




