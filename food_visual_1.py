from plotly.graph_objs import Bar, Layout
from plotly import offline
from filter_cost_abroad import food_costs

food_costs = food_costs()

#Visualise the results.

x_values = [x[0] for x in food_costs]
y_values = [x[1] for x in food_costs]
data = [Bar(x=x_values, y=y_values)]

x_axis_config = {'title': 'Country'}
y_axis_config = {'title': 'Food Price Level (EU28 Average = 100)'}
my_layout = Layout(title='Relative food price levels in the EU - 2018',
	xaxis=x_axis_config, yaxis=y_axis_config)
offline.plot({'data': data, 'layout': my_layout}, filename='food.html')
