import json
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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


euimage = (
    "https://raw.githubusercontent.com/jonboland/cost-abroad/master/euromapblur.png"
)

about = [
    html.P(
        "Cost Abroad is a tool for visualising information about the relative "
        "day-to-day costs of visiting different countries in Europe.",
        className="card-text",
    ),
    html.P(
        "There are wide variations in the cost of food, accommodation and transport etc. "
        "between European countries, so being able to get a simple overview of these "
        "differences in map form can help with planning trips and budgeting when travelling "
        "on holiday or business.",
        className="card-text",
    ),
    html.P(
        "Data is drawn from eurostat's price level indices (PLIs), "
        "which are based on a country's purchasing power parity divided by "
        "its current nominal exchange rate. PLIs are not intended to rank countries strictly, "
        "but provide a good indication of the order of magnitude of the price level "
        "in one country in relation to others.",
        className="card-text",
    ),
]

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
            style={"display": "flex", "justify-content": "center"},
        ),
        dcc.Graph(
            id="my-graph",
            style={
                "width": 650,
                "margin-left": "auto",
                "padding-left": 45,
                "margin-right": "auto",
            },
        ),
        dbc.Card(
            [
                dbc.CardImg(
                    src=euimage,
                    style={
                        "filter": "grayscale(100%) brightness(130%)",
                        "border-radius": 0,
                    },
                ),
                dbc.CardBody(
                    [
                        html.H4("About", className="card-title"),
                        html.P(
                            "Cost Abroad is a tool for visualising information about "
                            "the relative day-to-day costs of visiting "
                            "different countries in Europe.",
                            className="card-text",
                        ),
                        dbc.Button(
                            "Read More",
                            id="open",
                            color="primary",
                            outline=True,
                            className="mr-1",
                            style={"margin": "auto", "width": "100%"},
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("About Cost Abroad"),
                                dbc.ModalBody(about),
                                dbc.ModalFooter(
                                    dbc.Button("Close", id="close", className="ml-auto")
                                ),
                            ],
                            id="modal",
                        ),
                    ]
                ),
            ],
            style={
                "width": 564,
                "margin-top": 15,
                "margin-left": "auto",
                "padding-left": 0,
                "margin-right": "auto",
                "border-radius": 0,
            },
        ),
    ],
    className="container",
)


############################## CALLBACKS/FIGURE #################################


@app.callback(
    Output("my-graph", "figure"),
    [Input("value-selected", "value")],
)
def update_figure(selected):
    """Generates choropleth based on selected option."""
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
            font={"size": 12},
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


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    """Provides open and close functionality for about section."""
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
