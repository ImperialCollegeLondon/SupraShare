import dash_bio as dashbio
from dash import callback, dcc
from dash.dependencies import MATCH, Input, Output

from .components import _mol_smiles


def _jsme_smiles(id_index: int) -> dcc.Store:
    """An intermediate data storage for a smiles string.

    The string is saved here after it is drawn on the jsme editor.

    Args:
        id_index (int): Index for the id of the Store. Will match its accompanying
            target component.

    Returns:
        dcc.Store: The storage object.
    """
    return dcc.Store(id=dict(type="jsme-smiles", index=id_index))


def jsme_drawer(id_index: int) -> list:
    """A container for the jsme molecule drawer/editor.

    The container is filled from its accompanying _mol_smiles data store via the
    `draw_molecule` callback, if a corresponding upload button exists.

    Args:
        id_index (int): Index for the component ID - allows for multiple images

    Returns:
        list: List containing the data store and the jsme object.
    """
    return [_mol_smiles(id_index), dashbio.Jsme(id=dict(type="jsme", index=id_index))]


@callback(
    Output({"type": "jsme-smiles", "index": MATCH}, "data"),
    Input({"type": "jsme", "index": MATCH}, "eventSmiles"),
)
def save_smiles(smiles: str) -> str:
    """Save the SMILES string from the jsme editor in the mol-smiles data store."""
    return smiles


@callback(
    Output({"type": "jsme", "index": MATCH}, "smiles"),
    Input({"type": "mol-smiles", "index": MATCH}, "data"),
)
def draw_molecule(smiles: str) -> str:
    """Updates the molecular structure in the jsme editor to match mol-smiles.

    Args:
        smiles (str): A SMILES String.

    Returns:
        str: A SMILES string that the jsme editor converts into a molecular structure.
    """
    return smiles
