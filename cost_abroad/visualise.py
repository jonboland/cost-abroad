import json
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


# Load all cost category data
path = Path(__file__).parent.parent / "data" / "combined.txt"
with open(path, mode="r") as json_file:
    price_levels = json.load(json_file)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colours = ("reds", "magenta", "greens", "blues", "purples", "teal")
categories = reversed(tuple(price_levels.keys()))
complete = dict(zip(categories, colours))


############################### PAGE COMPONENTS ################################

app.layout = html.Div(
    [
        html.Div(
            [html.H1("Cost Abroad")], style={"textAlign": "center", "margin-top": 20}
        ),
        html.Div(
            "Select a category then hover over countries "
            "to see how their prices compare to the EU average.",
            style={"textAlign": "center"},
        ),
        html.Div(
            "The average price across all EU member states is equivalent to 100.",
            style={"textAlign": "center"},
        ),
        html.Div(
            [
                html.H6(
                    dcc.RadioItems(
                        id="value-selected",
                        value="overall",
                        options=[
                            {
                                "label": "Restaurants & Hotels"
                                if x == "restaurant_hotel"
                                else x.title(),
                                "value": x,
                            }
                            for x in complete
                        ],
                        labelStyle={"display": "inline-block", "margin-bottom": "0px"},
                        inputStyle={"margin-left": "10px", "margin-right": "3px"},
                        style={
                            "textAlign": "center",
                            "width": "auto",
                            "margin-top": 10,
                        },
                        className="six columns",
                    )
                )
            ],
            className="row",
            style={"display": "flex", "justifyContent": "center"},
        ),
        dcc.Graph(
            id="my-graph",
            style={
                "width": 650,
                "margin-left": "auto",
                "padding-left": 48,
                "margin-right": "auto",
            },
        ),
    ],
    className="container",
)


############################## CALLBACK/FIGURE #################################


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("value-selected", "value")],
)
def update_figure(selected):
    """Generate choropleth based on selected option."""
    x_values = [x[0] for x in price_levels[selected]]
    y_values = [x[1] for x in price_levels[selected]]

    trace = go.Choropleth(
        type="choropleth",
        locations=x_values,
        locationmode="country names",
        colorscale=complete[selected],
        colorbar=go.choropleth.ColorBar(ticksuffix="", title="Percent", len=0.5),
        z=y_values,
    )

    return {
        "data": [trace],
        "layout": go.Layout(
            height=650,
            width=650,
            font={"size": 14},
            margin={"t": 0, "b": 0, "l": 0, "r": 0},
            geo={
                "lataxis": {"range": [36.0, 71.0]},
                "lonaxis": {"range": [-10.0, 35.0]},
                "projection": {"type": "transverse mercator"},
                "resolution": 50,
                "showcoastlines": True,
                "showframe": True,
                "showcountries": True,
            },
        ),
    }


if __name__ == "__main__":
    app.run_server(debug=True)
