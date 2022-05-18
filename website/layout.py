import os
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

url_prefix = os.getenv("URL_PREFIX", "")

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Is My Cage Porous?", href=url_prefix, active=True)),
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

with open(Path(__file__).parent / "static" / "index.md", "r") as f:
    md = f.readlines()


def content():
    return [
        dcc.Markdown(md),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(src=dash.get_asset_url("cavity.png"), height="250px"),
                        dbc.Label(
                            "CC3, a shape persistent cage with cavity highlighted in red."
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Img(
                            src=dash.get_asset_url("collapsed.png"), height="250px"
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
                        dbc.Col(dbc.Label("Building Block SMILES", width="auto")),
                        dbc.Col(dbc.Label("Model", width="auto")),
                        dbc.Col(),
                        dbc.Col(dbc.Label("Result", width="auto")),
                    ],
                ),
            ],
        ),
        dbc.Button("Add Row", id="add-button"),
        html.Br(),
        dbc.Col(dbc.Button(dcc.Upload("Upload .mol file", id="file-upload"))),
        html.Img(id="mol-image"),
        dbc.Label(id="mol-smiles"),
        dbc.Col(id="jsme-div"),
        dbc.Label(id="jsme-smiles"),
        html.Br(),
    ]


def layout():
    return html.Div(
        children=[
            navbar,
            html.Br(),
            dbc.Container(
                children=content(),
            ),
            html.Br(),
            html.Footer(
                dbc.NavbarSimple(dbc.NavItem("Imperial College London"), color="light")
            ),
        ]
    )
