from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from .components import captioned_image_row

with open(Path(__file__).parent / "static" / "index.md", "r") as f:
    md = f.readlines()


def content():
    images_and_captions = [
        dict(
            src=dash.get_asset_url("cavity.png"),
            caption="CC3, a shape persistent cage with cavity highlighted in red.",
        ),
        dict(
            src=dash.get_asset_url("collapsed.png"),
            caption="A collapsed cage lacking a central cavity.",
        ),
    ]
    return [
        dcc.Markdown(md),
        captioned_image_row(images_and_captions),
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
