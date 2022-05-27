from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import dcc

from .components import captioned_image_row, mol_file_upload_button, mol_image
from .drawer import jsme_drawer


def content() -> list:
    """Generate the content for the webpage.

    Returns:
        list: A list of each component ordered from the top of the page to the bottom.
    """
    # Read the static markdown content in static/index.md for the top of the webpage.
    # Edit that file to modify the text content at the top of the page.
    with open(Path(__file__).parent / "static" / "index.md", "r") as f:
        md = f.readlines()

    # Images and captions in a format that can be used by `captioned_imaged_row`
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

    table_headers = [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Label("Linker SMILES", width="auto"),
                    style={"text-align": "center"},
                ),
                dbc.Col(
                    dbc.Label("Building Block SMILES", width="auto"),
                    style={"text-align": "center"},
                ),
                dbc.Col(
                    dbc.Label("Model", width="auto"),
                    style={"text-align": "center"},
                ),
                dbc.Col(),
                dbc.Col(
                    dbc.Label("Result", width="auto"),
                    style={"text-align": "center"},
                ),
            ],
        )
    ]

    return [
        dcc.Markdown(md),
        captioned_image_row(images_and_captions),
        dbc.Card(table_headers, id="run-card"),
        dbc.Button("Add Row", id="add-button", class_name="me-1"),
        # How to include a file upload button and corresponding image:
        mol_file_upload_button("Upload .mol file", id_index=0),
        mol_image(id_index=0),  # Note: id_index must match above
        # How to include a file upload button and corresponding jsme drawer:
        mol_file_upload_button("Upload .mol file", id_index=1),
        jsme_drawer(id_index=1),
    ]
