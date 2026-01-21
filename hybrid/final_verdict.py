def hybrid_verdict(risk_score, iforest_prediction):
    """
    iforest_prediction: -1 = anomaly, 1 = normal
    """

    if risk_score >= 80:
        return "HIGH RISK", "Static analysis detected high-severity vulnerability"

    if risk_score >= 50 and iforest_prediction == -1:
        return "HIGH RISK", "Suspicious behavior confirmed by anomaly detection"

    if risk_score >= 50:
        return "MEDIUM RISK", "Conservative static risk detected"

    if iforest_prediction == -1:
        return "MEDIUM RISK", "Anomalous contract behavior detected"

    return "LOW RISK", "No significant risk patterns detected"
