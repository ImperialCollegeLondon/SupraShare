import dash_bootstrap_components as dbc
from dash import dcc, html

from .model import predict


def jsme(id=None):
    try:
        import dash_bio as dashbio

        return dashbio.Jsme(id=id)
    except ImportError:
        return html.Img(id=id)
