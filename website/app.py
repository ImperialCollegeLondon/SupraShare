import os
import pickle
from glob import iglob

import rdkit.Chem.AllChem as rdkit
from flask import Flask, current_app, redirect, request, url_for


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


def fingerprint():
    bb = rdkit.AddHs(rdkit.MolFromSmiles(request.form["bb"]))
    lk = rdkit.AddHs(rdkit.MolFromSmiles(request.form["lk"]))
    return [bb_count_fingerprint((bb, lk), 512, 8)]


def load_models():
    models = {}
    for model_path in iglob("models/*.pkl"):
        name, _ = os.path.splitext(os.path.basename(model_path))
        with open(model_path, "rb") as f:
            models[name] = pickle.load(f)
    return models


app = Flask(__name__, instance_relative_config=True)
app.models = load_models()


@app.route("/")
def root():
    return redirect(url_for("static", filename="index.html"))


@app.route("/predict/<model_name>", methods=["POST"])
def predict(model_name):
    ans = current_app.models[model_name].predict(fingerprint())
    return str(ans[0])


if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port, debug=True)
    app.run()
