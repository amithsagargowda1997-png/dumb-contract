def compute_risk_score(features):
    score = 0
    reasons = []

    if features["num_reentrancy_flags"] > 0:
        score += 40
        reasons.append("Reentrancy risk detected")

    if features["num_external_calls"] > 0:
        score += 20
        reasons.append("Low-level external calls present")

    if features["num_loops"] > 0:
        score += 15
        reasons.append("Loop constructs detected")

    if features["num_loops_with_external_calls"] > 0:
        score += 30
        reasons.append("External calls inside loops (gas-DoS risk)")

    if features["num_public_functions"] > 3:
        score += 10
        reasons.append("Large public attack surface")

    return score, reasons
