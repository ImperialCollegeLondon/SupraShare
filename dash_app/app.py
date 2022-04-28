import os
from pathlib import Path

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate
from flask import Flask
import plotly.express as px


url_prefix = os.getenv("URL_PREFIX", "")

server = Flask(__name__)
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    server=server,
    requests_pathname_prefix=url_prefix + "/",
    routes_pathname_prefix=url_prefix + "/",
    # suppress_callback_exceptions=True,
)


# Navbar across the top of the page. Includes logo and dropdown to select model
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Is My Cage Porous?", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="SupraShare",
    brand_href="#",
    color="primary",
    dark=True,
)

with open("dash_app/index.md", "r") as f:
    md = f.readlines()

# Master layout for the whole dashboard. Includes the navbar and a container that holds
# loading spinners and space for the inputs and graphs.
app.layout = html.Div(
    children=[
        navbar,
        html.Br(),
        dbc.Container(
            # fluid=True,
            children=[
                dcc.Markdown(md),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(
                                    src=app.get_asset_url("cavity.png"), height="300px"
                                ),
                                dbc.Label(
                                    "CC3, a shape persistent cage with cavity highlighted in red."
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Img(
                                    src=app.get_asset_url("collapsed.png"),
                                    height="300px",
                                ),
                                dbc.Label("A collapsed cage lacking a central cavity."),
                            ]
                        ),
                    ]
                ),
                html.Br(),
                dbc.Card(
                    id="run-card",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Linker SMILES", width="auto")),
                                dbc.Col(
                                    dbc.Label("Building Block SMILES", width="auto")
                                ),
                                dbc.Col(dbc.Label("Model", width="auto")),
                                dbc.Col(),
                                dbc.Col(dbc.Label("Result", width="auto")),
                            ],
                        ),
                    ],
                ),
                dbc.Button("Add Row", id="add-button"),
                html.Br(),
            ],
        ),
    ]
)


@app.callback(
    Output("run-card", "children"),
    Input("add-button", "n_clicks"),
    State("run-card", "children"),
)
def add_row(n_clicks, children):
    if n_clicks is None:
        n_clicks = 0

    form = dbc.Form(
        dbc.Row(
            [
                dbc.Col(
                    dbc.Input(type="text"),
                ),
                dbc.Col(
                    dbc.Input(type="text"),
                ),
                dbc.Col(
                    [
                        dbc.Select(
                            id="model-dropdown",
                            value="amine2aldehyde3",
                            options=[
                                {"label": model.stem, "value": model.stem}
                                for model in Path("models").glob("*")
                            ],
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Run Model \U0001F680",
                            id=dict(type="run-button", index=n_clicks),
                            color="primary",
                        )
                    ],
                    class_name="d-grid gap-2",
                ),
                dbc.Col(
                    dbc.Label(
                        id=dict(type="result", index=n_clicks),
                    )
                ),
            ],
            align="center",
        )
    )
    return children + [form]


@app.callback(
    Output({"type": "result", "index": MATCH}, "children"),
    Input({"type": "run-button", "index": MATCH}, "n_clicks"),
    State({"type": "run-button", "index": MATCH}, "id"),
)
def run_model(n_clicks, button_id):
    if n_clicks is None:
        raise PreventUpdate

    return button_id["index"]


if __name__ == "__main__":
    app.run_server(debug=True)
