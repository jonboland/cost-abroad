import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from create_cost_abroad import categories


external_stylesheets = ['https://codepen.io/jonboland/pen/yLyxpZa.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Load all cost category data
with open('combined.txt') as json_file:
        price_levels = json.load(json_file)

# Add overall to selected categories
# (Categories are selected when price files are originally created)
complete = {**{'overall': 'reds'}, **{k:v[1] for k,v in categories.items()}}


################################ PAGE COMPONENTS ###############################

app.layout = html.Div([

    html.Div([
        html.H1('Cost Abroad')
    ], style={'textAlign': 'center', 'padding-bottom': 0}),

    html.Div('Select a category and hover over countries '
        'to see how their prices compare to the EU average.', 
        style={'textAlign': 'center'}),

    html.Div('The average price across all EU member states '
        'is equivalent to 100.', 
        style={'textAlign': 'center'}),

    html.Div([
        html.H6(dcc.RadioItems(
            id='value-selected',
            value='overall',
            options=[{'label': 'Restaurants & Hotels' if x == 'restaurant_hotel' 
                      else x.title(), 'value': x} for x in complete],
            labelStyle={'display': 'inline-block'},
            style={'display': 'block', 'margin-left': 140,
                   'margin-right': 'auto', 'width': '70%'},
            className='six columns',
        )  
    )], className='row'),

    dcc.Graph(id='my-graph')

], className='container')


############################## CALLBACK/FIGURE #################################

@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('value-selected', 'value')]
)

def update_figure(selected):
    """Generate choropleth based on selected option."""
    x_values = [x[0] for x in price_levels[selected]]
    y_values = [x[1] for x in price_levels[selected]]

    trace = go.Choropleth(
        type='choropleth',
        locations=x_values,
        locationmode='country names',
        colorscale=complete[selected],
        colorbar=go.choropleth.ColorBar(
                    ticksuffix='',
                    title='Percent',
                    len=0.5),
        z=y_values,
    )

    return {'data': [trace],
            'layout': go.Layout(
                    height=900,
                    width=900,
                    font={'size': 16},
                    margin={'t': 0, 'b': 185, 'l': 150, 'r': 50},
                    geo={'lataxis': {'range': [36.0, 71.0]},
                         'lonaxis': {'range': [-10.0, 35.0]},
                         'projection': {'type': 'transverse mercator'},
                         'resolution': 50,
                         'showcoastlines': True,
                         'showframe': True,
                         'showcountries': True,
                    }
            )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
