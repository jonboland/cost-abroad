import plotly as py
import plotly.graph_objs as go
from combine_cost_abroad import combined_values


price_levels = combined_values()

categories = (
              ('overall', 'reds'),
              ('food', 'magenta'),
              ('alcohol', 'greens'),
              ('transport', 'blues'),
              ('recreation', 'purples'),
              ('restaurant_hotel', 'teal'),
)

for category in categories:

    x_values = [x[0] for x in price_levels[category[0]]]
    y_values = [x[1] for x in price_levels[category[0]]]
    color = category[1]

    data = {
        'type': 'choropleth',
        'locations': x_values,
        'locationmode': 'country names',
        'colorscale': color,
        'colorbar': go.choropleth.ColorBar(
            ticksuffix='%',
            title='',
            len=0.5,
        ),
        'z': y_values,
    }

    layout = {
        'height': 900,
        'width': 900,
        'title': f'Relative Cost Compared to EU Average - {category[0]}',
        'font': {'size': 16},
        'margin': {"t": 50, "b": 50, "l": 50, "r": 50},
        'geo': {
            'lataxis': {'range': [36.0, 71.0]},
            'lonaxis': {"range": [-10.0, 35.0]},
            'projection': {'type': 'transverse mercator'},
            'resolution': 50,
            'showcoastlines': True,
            'showframe': True,
            'showcountries': True,
        }
    }

    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig)
