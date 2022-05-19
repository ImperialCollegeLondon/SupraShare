from pathlib import Path

import dash_bootstrap_components as dbc
from dash import callback
from dash.dependencies import MATCH, Input, Output, State
from dash.exceptions import PreventUpdate

from .model import predict


@callback(
    Output("run-card", "children"),
    Input("add-button", "n_clicks"),
    State("run-card", "children"),
)
def add_row(n_clicks: int, children: list) -> list:
    """Adds a row to the card with the model results when "Add Row" button is clicked.

    Each object in the row is provided with a dictionary id so that they can be used
    correctly with pattern-matching callbacks.

    Args:
        n_clicks (int): Increments on a button click. The trigger for this callback.
        children (list): The children of the card. Contains dbc.Row or dbc.Form.

    Returns:
        list: The updated children. Equivalent to the input children plus a Form/Row
    """
    if n_clicks is None:
        n_clicks = 0

    form = dbc.Form(
        dbc.Row(
            [
                dbc.Col(
                    dbc.Input(type="text", id=dict(type="lk", index=n_clicks)),
                ),
                dbc.Col(
                    dbc.Input(type="text", id=dict(type="bb", index=n_clicks)),
                ),
                dbc.Col(
                    [
                        dbc.Select(
                            id=dict(type="model-dropdown", index=n_clicks),
                            value="amine2aldehyde3",
                            options=[
                                {"label": model.stem, "value": model.stem}
                                for model in Path("models").glob("*")
                            ],
                        ),
                    ]
                ),
                dbc.Col(
                    dbc.Button(
                        "Run Model \U0001F680",
                        id=dict(type="run-button", index=n_clicks),
                        color="primary",
                    ),
                    class_name="d-grid gap-2",
                ),
                dbc.Col(dbc.Spinner(dbc.Label(id=dict(type="result", index=n_clicks)))),
            ],
            align="center",
        )
    )
    return children + [form]


@callback(
    Output({"type": "result", "index": MATCH}, "children"),
    Input({"type": "run-button", "index": MATCH}, "n_clicks"),
    State({"type": "model-dropdown", "index": MATCH}, "value"),
    State({"type": "bb", "index": MATCH}, "value"),
    State({"type": "lk", "index": MATCH}, "value"),
)
def run_model(n_clicks: int, model_name: str, bb: str, lk: str) -> dbc.Label:
    """Runs the model when the "Run Model" button is clicked and displays the result.

    Since there are potentially multiple "Run Model" buttons, we need to know which one
    was clicked so we can fill in the corresponding result box. This is done using
    Pattern-Matching Callbacks (see: https://dash.plotly.com/pattern-matching-callbacks)

    Args:
        n_clicks (int): Increments on a button click. The trigger for this callback.
        model_name (str): The name of the desired model to run
        bb (str): The Building Block SMILES string.
        lk (str): The Linker SMILES string.

    Raises:
        PreventUpdate: Prevents the callback from being run automatically on page load.

    Returns:
        dbc.Label: A label with the result of the model. Possible Answers:
            - INVALID INPUT
            - COLLAPSED
            - SHAPE PERSISTENT
            - MODEL ERROR
    """
    if n_clicks is None or bb is None or lk is None:
        raise PreventUpdate

    try:
        result = predict(model_name, bb, lk)
    except ValueError:
        return dbc.Label("INVALID INPUT", color="warning")

    if result == 1:
        return dbc.Label("COLLAPSED", color="danger")
    if result == 0:
        return dbc.Label("SHAPE PERSISTENT", color="success")
    return dbc.Label("MODEL ERROR", color="warning")
