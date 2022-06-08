import pytest
import rdkit.Chem.AllChem as rdkit

from website.model import bb_count_fingerprint, load_models


@pytest.mark.skip(reason="This is just an example")
def test_load_models():
    models = load_models()
    assert len(models) == 6


@pytest.mark.skip(reason="This is just an example")
def test_predict():
    model = load_models()["amine2aldehyde3"]
    bb = rdkit.AddHs(rdkit.MolFromSmiles("O=Cc1cc(C=O)cc(C=O)c1"))

    # Model returns 0 for persistent cage
    lk = rdkit.AddHs(rdkit.MolFromSmiles("N[C@H]1CCCC[C@@H]1N"))
    persistent_fingerprint = bb_count_fingerprint((bb, lk), 512, 8)
    assert model.predict([persistent_fingerprint]) == 0

    # Model returns 1 for collapsed cage
    lk = rdkit.AddHs(rdkit.MolFromSmiles("NCCCCCCN"))
    collapsed_fingerprint = bb_count_fingerprint((bb, lk), 512, 8)
    assert model.predict([collapsed_fingerprint]) == 1
