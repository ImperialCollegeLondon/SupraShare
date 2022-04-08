# Simple Dash example from https://dash.plotly.com/layout
import flask
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

server = flask.Flask(__name__)  # define flask app.server

app = Dash(__name__, server=server)  # call flask server

# Run in production with gunicorn example.graph:server -b :8050

colors = {"background": "#111111", "text": "#7FDBFF"}

df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
    font_color=colors["text"],
)

app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            children="Hello",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Div(
            children="Dash: A web application framework for your data.",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        dcc.Graph(id="example-graph-2", figure=fig),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
