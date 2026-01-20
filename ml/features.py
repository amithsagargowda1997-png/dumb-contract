def extract_features(
    call_graph,
    external_calls,
    reentrancy_vulns,
    gas_loops,
    function_visibility
):
    features = {}

    features["num_functions"] = len(function_visibility)

    features["num_public_functions"] = sum(
        1 for v in function_visibility.values()
        if v in ("public", "external")
    )

    features["num_external_calls"] = len(external_calls)

    features["num_reentrancy_flags"] = len(reentrancy_vulns)

    features["num_loops"] = len(gas_loops)

    features["num_loops_with_external_calls"] = sum(
        1 for g in gas_loops if g.get("external_call_inside")
    )

    return features
