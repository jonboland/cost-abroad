"""
Trigger the creation of all individual CostAbroad price files
and a combined file including an overall category.
"""

from cost_abroad.create import create_price_files
from cost_abroad.combine import create_combined_file


CATEGORIES = {
    "restaurant_hotel": "A0111",
    "recreation": "A0109",
    "transport": "A0107",
    "alcohol": "A010201",
    "food": "A010101",
}


def main():
    create_price_files(**CATEGORIES)
    create_combined_file(**CATEGORIES)


if __name__ == '__main__':
    main()
