import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from combine_cost_abroad import combined_values


external_stylesheets = ['https://codepen.io/jonboland/pen/yLyxpZa.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Import dictionary containing cost categories
price_levels = combined_values()

color = {'overall': 'reds', 'food': 'magenta',
         'alcohol': 'greens', 'transport': 'blues',
         'recreation': 'purples', 'restaurant_hotel': 'teal'}


############################### PAGE COMPONENTS ##############################

app.layout = html.Div([

    html.Div([
        html.H1('Cost Abroad')
    ], style={'textAlign': 'center', 'padding-bottom': 30}),

    html.Div([
        html.Span(
            'Category : ',
            className='six columns',
            style={'text-align': 'right',
                   'width': '40%', 'padding-top': 5}
        ),
        dcc.Dropdown(
            id='value-selected',
            value='overall',
            options=[
                {'label': 'Overall ', 'value': 'overall'},
                {'label': 'Food', 'value': 'food'},
                {'label': 'Alcohol', 'value': 'alcohol'},
                {'label': 'Transport', 'value': 'transport'},
                {'label': 'Recreation', 'value': 'recreation'},
                {'label': 'Restaurants & Hotels', 'value': 'restaurant_hotel'}
            ],
            style={'display': 'block', 'margin-left': 'auto',
                   'margin-right': 'auto', 'width': '70%'},
            className='six columns',
        )
    ], className='row'),

    dcc.Graph(id='my-graph')

], className='container')


############################# CALLBACK/FIGURE ################################

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
        colorscale=color[selected],
        colorbar=go.choropleth.ColorBar(
                    ticksuffix='%',
                    title='',
                    len=0.5),
        z=y_values,
    )

    return {'data': [trace],
            'layout': go.Layout(
                    height=900,
                    width=900,
                    font={'size': 16},
                    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
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
