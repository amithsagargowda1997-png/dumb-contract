from analysis.ast import parse_solidity, find_external_calls,get_function_visibility
from analysis.call_graph import build_call_graph
from analysis.reentrancy import detect_reentrancy
from analysis.gas_analysis import detect_gas_loops
from ml.features import extract_features
from hybrid.decision import compute_risk_score
import sys


if __name__ == "__main__":
    contract_path = sys.argv[1]

    ast = parse_solidity(contract_path)
    calls = find_external_calls(ast)
    graph = build_call_graph(ast)
    visibility = get_function_visibility(ast)
    gas_loops = detect_gas_loops(ast)

    print("External Calls Found:")
    for c in calls:
        print(f"Function: {c['function']} | Type: {c['call_type']} | Src: {c['line']}")

    print("\nFunction Call Graph:")
    for caller, callees in graph.items():
        for callee in callees:
            print(f"{caller} -> {callee}")
    vulnerable = detect_reentrancy(graph, calls,visibility)

    print("\nReentrancy Vulnerabilities:")
    for f in vulnerable:
        print(f"⚠️  Potential reentrancy in function: {f}")
    
    print("\nGas Limit / Loop-Based Risks:")
    for g in gas_loops:
        risk = "HIGH" if g["external_call_inside"] else "MEDIUM"
        print(
            f"⚠️  {risk} risk loop in function {g['function']} "
            f"({g['loop_type']})"
        )
    
    features = extract_features(
    call_graph=graph,
    external_calls=calls,
    reentrancy_vulns=vulnerable,
    gas_loops=gas_loops,
    function_visibility=visibility
    )

    print("\nML Feature Vector:")
    for k, v in features.items():
        print(f"{k}: {v}")
    
    risk_score, reasons = compute_risk_score(features)
    
    print("\nOverall Risk Score:", risk_score)
    
    print("Risk Reasons:")
    for r in reasons:
        print(f"- {r}")



