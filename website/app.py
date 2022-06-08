import os
from pathlib import Path

import dash_bootstrap_components as dbc
import yaml
from dash import Dash, html
from flask import Flask

from . import callbacks  # noqa: F401
from .layout import content

URL_PREFIX = os.getenv("URL_PREFIX", "") + "/"
APP_NAME = os.getenv("APP_NAME", "")

if (filepath := Path(__file__).parent.parent / "app_list.yaml").exists():
    with open(filepath, "r") as f:
        app_list = yaml.safe_load(f)
else:
    app_list = {}

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink(APP_NAME, href=URL_PREFIX, external_link=True, active=True)
        )
        if APP_NAME
        else None,
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem(name, href=link, external_link=True)
                for name, link in app_list.items()
                if name != APP_NAME
            ],
            nav=True,
            in_navbar=True,
            label="More",
        )
        if app_list
        else None,
    ],
    brand="SupraShare",
    brand_href="https://suprashare.rcs.ic.ac.uk/",
    color="primary",
    dark=True,
)

server = Flask(__name__)
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    server=server,
    requests_pathname_prefix=URL_PREFIX,
    routes_pathname_prefix=URL_PREFIX,
)


def layout():
    return html.Div(
        children=[
            html.Header(navbar),
            dbc.Container(
                [dbc.Row(dbc.Col(cc, class_name="gy-2")) for cc in content()]
            ),
            html.Footer(
                dbc.NavbarSimple(
                    dbc.NavItem("Imperial College London"),
                    color="light",
                )
            ),
        ]
    )


app.layout = layout

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
