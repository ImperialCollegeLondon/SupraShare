import os
import pickle
from glob import iglob

import rdkit.Chem.AllChem as rdkit


def bb_count_fingerprint(mols, bits, radius):
    """ """

    full_fp = []
    for mol in mols:
        rdkit.GetSSSR(mol)
        mol.UpdatePropertyCache(strict=False)
        info = {}
        fp = rdkit.GetMorganFingerprintAsBitVect(mol, radius, bits, bitInfo=info)
        fp = list(fp)
        for bit, activators in info.items():
            fp[bit] = len(activators)
        full_fp.extend(fp)
    full_fp.append(1)
    return full_fp


def fingerprint(bb, lk):
    bb = rdkit.MolFromSmiles(bb)
    lk = rdkit.MolFromSmiles(lk)
    if bb is None or lk is None:
        raise ValueError(
            "Invalid values for fingerprint: bb and lk must be valid SMILES strings"
        )
    bb = rdkit.AddHs(bb)
    lk = rdkit.AddHs(lk)
    return [bb_count_fingerprint((bb, lk), 512, 8)]


def load_models():
    models = {}
    for model_path in iglob("models/*.pkl"):
        name, _ = os.path.splitext(os.path.basename(model_path))
        with open(model_path, "rb") as f:
            models[name] = pickle.load(f)
    return models


def predict(model_name, bb, lk):
    ans = load_models()[model_name].predict(fingerprint(bb, lk))
    return ans[0]
