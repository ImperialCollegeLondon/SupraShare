import os

import dash_bootstrap_components as dbc
from dash import Dash, html
from flask import Flask

from . import callbacks  # noqa: F401
from .layout import content

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

server = Flask(__name__)
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    server=server,
    requests_pathname_prefix=url_prefix + "/",
    routes_pathname_prefix=url_prefix + "/",
)


def layout():
    if url_prefix == "":
        return html.Div(
            children=[
                html.Header(navbar),
                dbc.Container(dbc.Col(content())),
                html.Footer(
                    dbc.NavbarSimple(
                        dbc.NavItem("Imperial College London"),
                        color="light",
                    )
                ),
            ]
        )
    return dbc.Container(children=content())


app.layout = layout

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
