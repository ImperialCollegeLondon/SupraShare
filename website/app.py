import os
import pickle
from glob import iglob

import rdkit.Chem.AllChem as rdkit
from flask import Blueprint, Flask, current_app, redirect, render_template, request


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


url_prefix = os.getenv("URL_PREFIX", "")
if url_prefix:
    static_url_path = url_prefix + "/static"
else:
    static_url_path = "/static"

app = Flask(__name__, instance_relative_config=True, static_url_path=static_url_path)
app.models = load_models()

default_bp = Blueprint("default", __name__, template_folder="templates")


@default_bp.route("/")
def root():
    return render_template("index.html")


@default_bp.route("/predict/<model_name>", methods=["POST"])
def predict(model_name):
    ans = current_app.models[model_name].predict(fingerprint())
    return str(ans[0])


app.register_blueprint(default_bp, url_prefix=url_prefix)

if url_prefix:
    # if url_prefix assume running in production
    from werkzeug.middleware.proxy_fix import ProxyFix

    app = ProxyFix(app)  # enable choice of http(s) based on request headers

if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port, debug=True)
    app.run()
