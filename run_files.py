"""
Trigger the creation of individual CostAbroad price files
and a combined file including an overall category.

If  run directly all category files will be produced
and included in the combined file.

If run as a module one or more of the below keyword arguments
must be passed to the run_files function:

food='A010101'
alcohol='A010201'
transport='A0107'
recreation='A0109'
restaurant_hotel='A0111'
"""

from create_cost_abroad import create_price_files
from combine_cost_abroad import create_combined_file


categories = {'restaurant_hotel': 'A0111',
              'recreation': 'A0109',
              'transport': 'A0107',
              'alcohol': 'A010201',
              'food': 'A010101',
}


def run_files(**kwargs):
        create_price_files(**kwargs)
        create_combined_file(**kwargs)


if __name__ == '__main__':
        run_files(**categories)

