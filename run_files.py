"""
Trigger the creation of individual CostAbroad price files
and a combined file including an overall category.

If  run directly all category files will be produced
and included in the combined file.

If run as a module one or more of the below keyword arguments
must be passed to the run_files function:

food=['A010101', 'magenta'],
alcohol=['A010201', 'greens'],
transport=['A0107', 'blues'],
recreation=['A0109', 'purples'],
restaurant_hotel=['A0111', 'teal']
"""

from create_cost_abroad import create_price_files
from combine_cost_abroad import create_combined_file


categories = {'restaurant_hotel': ['A0111', 'teal'],
              'recreation': ['A0109', 'purples'],
              'transport': ['A0107', 'blues'],
              'alcohol': ['A010201', 'greens'],
              'food': ['A010101', 'magenta'],
}


def run_files(**kwargs):
    create_price_files(**kwargs)
    create_combined_file(**kwargs)


if __name__ == '__main__':
    run_files(**categories)

