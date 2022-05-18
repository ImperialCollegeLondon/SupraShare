import os

import dash_bootstrap_components as dbc
from dash import Dash
from flask import Flask

from . import callbacks
from .layout import layout

url_prefix = os.getenv("URL_PREFIX", "")

server = Flask(__name__)
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    server=server,
    requests_pathname_prefix=url_prefix + "/",
    routes_pathname_prefix=url_prefix + "/",
)


app.layout = layout


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
