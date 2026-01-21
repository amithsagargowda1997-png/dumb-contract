import os
import csv

from analysis.ast import parse_solidity, find_external_calls, get_function_visibility
from analysis.call_graph import build_call_graph
from analysis.reentrancy import detect_reentrancy
from analysis.gas_analysis import detect_gas_loops
from ml.features import extract_features
from hybrid.decision import compute_risk_score


CONTRACT_DIR = "contracts"
OUTPUT_FILE = "dataset.csv"


def analyze_contract(contract_path):
    try:
        ast = parse_solidity(contract_path)

        external_calls = find_external_calls(ast)
        call_graph = build_call_graph(ast)
        visibility = get_function_visibility(ast)
        gas_loops = detect_gas_loops(ast)

        reentrancy = detect_reentrancy(
            call_graph, external_calls, visibility
        )

        features = extract_features(
            call_graph=call_graph,
            external_calls=external_calls,
            reentrancy_vulns=reentrancy,
            gas_loops=gas_loops,
            function_visibility=visibility
        )

        risk_score, _ = compute_risk_score(features)
        features["risk_score"] = risk_score

        return features

    except Exception as e:
        print(f"Skipping {contract_path}: {e}")
        return None


def build_dataset():
    rows = []

    for root, _, files in os.walk(CONTRACT_DIR):
        for file in files:
            if file.endswith(".sol"):
                path = os.path.join(root, file)
                result = analyze_contract(path)
                if result:
                    rows.append(result)

    if not rows:
        print("No contracts processed.")
        return

    fieldnames = rows[0].keys()

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Dataset saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    build_dataset()
