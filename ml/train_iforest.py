import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from hybrid.final_verdict import hybrid_verdict
import joblib

DATASET_PATH = "dataset.csv"


def train_isolation_forest():
    # Load dataset
    df = pd.read_csv(DATASET_PATH)

    # Features only (no labels)
    feature_cols = [
        "num_functions",
        "num_public_functions",
        "num_external_calls",
        "num_reentrancy_flags",
        "num_loops",
        "num_loops_with_external_calls"
    ]

    X = df[feature_cols]

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=0.25,  # expect ~25% anomalies
        random_state=42
    )

    model.fit(X_scaled)

    # Anomaly scores (lower = more anomalous)
    scores = model.decision_function(X_scaled)
    predictions = model.predict(X_scaled)  # -1 = anomaly, 1 = normal

    df["iforest_score"] = scores
    df["iforest_prediction"] = predictions

    print("\nIsolation Forest Results:")
    print(df[feature_cols + ["risk_score", "iforest_score", "iforest_prediction"]])
    verdicts = []
    reasons = []
    
    for _, row in df.iterrows():
        verdict, reason = hybrid_verdict(
            risk_score=row["risk_score"],
            iforest_prediction=row["iforest_prediction"]
        )
        verdicts.append(verdict)
        reasons.append(reason)
    
    df["final_verdict"] = verdicts
    df["verdict_reason"] = reasons

    print(
    df[
        feature_cols
        + ["risk_score", "iforest_prediction", "final_verdict"]
    ]   
    )

    joblib.dump(model, "ml/iforest_model.joblib")
    joblib.dump(scaler, "ml/scaler.joblib")

    print("Saved Isolation Forest model and scaler")

    return df


if __name__ == "__main__":
    train_isolation_forest()
    import joblib



