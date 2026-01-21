from flask import Flask, render_template, request
import os
import tempfile
import joblib
import pandas as pd

from analysis.ast import parse_solidity, find_external_calls, get_function_visibility
from analysis.call_graph import build_call_graph
from analysis.reentrancy import detect_reentrancy
from analysis.gas_analysis import detect_gas_loops
from ml.features import extract_features
from hybrid.decision import compute_risk_score
from hybrid.final_verdict import hybrid_verdict

app = Flask(__name__)

# Load trained ML artifacts ONCE
iforest = joblib.load("ml/iforest_model.joblib")
scaler = joblib.load("ml/scaler.joblib")

FEATURE_ORDER = [
    "num_functions",
    "num_public_functions",
    "num_external_calls",
    "num_reentrancy_flags",
    "num_loops",
    "num_loops_with_external_calls",
]


@app.route("/", methods=["GET", "POST"])
def upload_contract():
    if request.method == "POST":
        file = request.files["contract"]

        if not file or not file.filename.endswith(".sol"):
            return "Invalid file type"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".sol") as tmp:
            file.save(tmp.name)
            path = tmp.name

        # ---- Static Analysis ----
        ast = parse_solidity(path)
        external_calls = find_external_calls(ast)
        call_graph = build_call_graph(ast)
        visibility = get_function_visibility(ast)
        gas_loops = detect_gas_loops(ast)
        reentrancy = detect_reentrancy(call_graph, external_calls, visibility)

        features = extract_features(
            call_graph,
            external_calls,
            reentrancy,
            gas_loops,
            visibility
        )

        # ---- Rule-based score ----
        risk_score, _ = compute_risk_score(features)

        # ---- ML Anomaly Detection ----
        X = pd.DataFrame([[features[f] for f in FEATURE_ORDER]],
                         columns=FEATURE_ORDER)

        X_scaled = scaler.transform(X)
        iforest_prediction = iforest.predict(X_scaled)[0]  # -1 or 1

        # ---- Hybrid Verdict ----
        verdict, reason = hybrid_verdict(risk_score, iforest_prediction)

        os.remove(path)

        return render_template(
            "result.html",
            external_calls=external_calls,
            reentrancy=reentrancy,
            gas_loops=gas_loops,
            features=features,
            risk_score=risk_score,
            iforest_prediction=iforest_prediction,
            verdict=verdict,
            reason=reason
        )

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
