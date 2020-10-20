import json
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


# Construct app
app = dash.Dash(__name__)


# Load cost category data
path = Path(__file__).resolve().parents[1] / "data" / "combined.txt"
with open(path, mode="r") as json_file:
    price_levels = json.load(json_file)


# Create cost categories dictionary
colours = ("reds", "magenta", "greens", "blues", "purples", "teal")
categories = reversed(tuple(price_levels.keys()))
complete = dict(zip(categories, colours))


############################### PAGE COMPONENTS ################################


heading = html.Div(
    [html.H1("Cost Abroad")], style={"textAlign": "center", "margin-top": 20}
)


intro_one = html.Div(
    "Select a category then hover over countries "
    "to see how their prices compare to the EU average.",
    style={"textAlign": "center"},
)


intro_two = html.Div(
    "The average price across all EU member states is equivalent to 100.",
    style={"textAlign": "center"},
)


# Cost category options in radio button format
category_selectors = html.Div(
    [
        html.H6(
            dcc.RadioItems(
                id="value-selected",
                # Default radio button value
                value="overall",
                # List of dictionaries containing the radio button labels and values
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
                style={"textAlign": "center", "width": "auto", "margin-top": 10},
            )
        )
    ],
    style={"display": "flex", "justify-content": "center"},
)


# Rendered map showing cost category date by country
eu_map = html.Div(
    dcc.Graph(
        id="my-graph",
        style={
            "max-width": 650,
            "margin-left": "auto",
            "padding-left": 44,
            "margin-right": "auto",
        },
    ),
)


# Image for about section
eu_image = (
    "https://raw.githubusercontent.com/jonboland/cost-abroad/master/euromapblur.png"
)


# Text and link for about section
about_text = [
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
    html.P("You can read more about these statistics here: ", className="card-text"),
    dbc.CardLink(
        "Price Level Indices",
        href="https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Price_level_index_(PLI)",
    ),
]


# Content container for about image, text and link
about_section = html.Div(
    dbc.Card(
        [
            dbc.CardImg(
                src=eu_image,
                style={
                    "filter": "grayscale(100%) brightness(130%)",
                    "border-radius": 0,
                },
            ),
            dbc.CardBody(
                [
                    html.H4("About Cost Abroad", className="card-title"),
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
                            dbc.ModalBody(about_text),
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
            "max-width": 567,
            "margin-top": 0,
            "margin-left": "auto",
            "margin-right": "auto",
            "border-radius": 0,
        },
    ),
)


# Text and link for issues and ideas section
issues_text = [
    html.P(
        "Comments regarding any problems you have encountered while using Cost Abroad, "
        "and ideas about how it could be enhanced, are welcome.",
        className="card-text",
    ),
    html.P(
        "To share these please either open an issue or submit a pull request via the project's "
        "GitHub repository:",
        className="card-text",
    ),
    dbc.CardLink("Cost Abroad Repo", href="https://github.com/jonboland/cost-abroad"),
]


# Content container for issues and ideas text and link
issues_section = html.Div(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Issues and Ideas", className="card-title"),
                    html.P(
                        "Do you have an issue to raise or an ideas you would like to share?",
                        className="card-text",
                    ),
                    dbc.Button(
                        "Discover How",
                        id="opentwo",
                        color="secondary",
                        className="mr-1",
                        style={"margin": "auto", "width": "100%"},
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Issues and Ideas"),
                            dbc.ModalBody(issues_text),
                            dbc.ModalFooter(
                                dbc.Button("Close", id="closetwo", className="ml-auto")
                            ),
                        ],
                        id="modaltwo",
                    ),
                ]
            ),
        ],
        style={
            "max-width": 567,
            "margin-top": 40,
            "margin-bottom": 30,
            "margin-left": "auto",
            "margin-right": "auto",
            "border-radius": 0,
        },
        color="light",
    ),
)


# Copyright notice
copyright = html.P(
    "© Jon Boland 2020",
    style={
        "max-width": 567,
        "margin-left": "auto",
        "margin-right": "auto",
        "padding-left": 18,
        "color": "#808080",
    },
)

################################## PAGE LAYOUT #################################

app.title = "Cost Abroad"

app.layout = html.Div(
    [
        heading,
        intro_one,
        intro_two,
        category_selectors,
        eu_map,
        about_section,
        issues_section,
        copyright,
    ],
)


################################# CALLBACKS/MAP ################################


@app.callback(
    Output("my-graph", "figure"), [Input("value-selected", "value")],
)
def update_figure(selected):
    """Generates choropleth map based on selected option."""
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


@app.callback(
    Output("modaltwo", "is_open"),
    [Input("opentwo", "n_clicks"), Input("closetwo", "n_clicks")],
    [State("modaltwo", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    """Provides open and close functionality for issues and ideas section."""
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=False)
