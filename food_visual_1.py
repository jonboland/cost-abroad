import json
import plotly as py
import plotly.graph_objs as go
from filter_cost_abroad import food_costs

food_costs = food_costs()

x_values = [x[0] for x in food_costs]
y_values = [x[1] for x in food_costs]

data = {
    'type': 'choropleth',
    'locations': x_values,
    'locationmode': 'country names',
    'colorscale': 'Reds',
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
    'margin': {"t": 50, "b": 50, "l": 50, "r": 50},
    'geo': {
        'lataxis': {'range': [36.0, 65.0]}, 
        'lonaxis': {"range": [-30.0, 36.0]}, 
        'projection': {'type': 'transverse mercator'}, 
        'resolution': 50, 
        'showcoastlines': True, 
        'showframe': True, 
        'showcountries': True,
    }
}

fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig)
