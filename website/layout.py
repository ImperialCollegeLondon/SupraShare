from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

with open(Path(__file__).parent / "static" / "index.md", "r") as f:
    md = f.readlines()


def image_row():
    return dbc.Row(
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
                    html.Img(src=dash.get_asset_url("collapsed.png"), height="250px"),
                    dbc.Label("A collapsed cage lacking a central cavity."),
                ]
            ),
        ]
    )


def content():
    return [
        dcc.Markdown(md),
        image_row(),
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
