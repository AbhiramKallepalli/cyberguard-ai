import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import shap

# Plain English translations for KDD feature names
FEATURE_TRANSLATIONS = {
    "duration": "connection lasted unusually long",
    "protocol_type": "unusual network protocol used",
    "service": "unusual service targeted",
    "flag": "connection ended abnormally",
    "src_bytes": "unusually large amount of data sent",
    "dst_bytes": "unusually large amount of data received",
    "land": "suspicious same-source-destination connection",
    "wrong_fragment": "fragmented packets detected",
    "urgent": "urgent packets flagged",
    "hot": "sensitive areas of system accessed",
    "num_failed_logins": "multiple failed login attempts",
    "logged_in": "login status was unusual",
    "num_compromised": "multiple compromised conditions detected",
    "root_shell": "root shell access attempted",
    "su_attempted": "superuser access attempted",
    "num_root": "high number of root accesses",
    "num_file_creations": "unusually high file creation activity",
    "num_shells": "multiple shell sessions opened",
    "num_access_files": "unusual number of files accessed",
    "num_outbound_cmds": "unusual outbound commands detected",
    "is_host_login": "host login detected",
    "is_guest_login": "guest login detected",
    "count": "high number of connections to same host",
    "srv_count": "high number of connections to same service",
    "serror_rate": "high rate of SYN errors",
    "srv_serror_rate": "high SYN error rate on service",
    "rerror_rate": "high rate of REJ errors",
    "srv_rerror_rate": "high REJ error rate on service",
    "same_srv_rate": "unusual same-service connection rate",
    "diff_srv_rate": "connecting to many different services",
    "srv_diff_host_rate": "service accessed from many different hosts",
    "dst_host_count": "high connections to destination host",
    "dst_host_srv_count": "high service connections to destination",
    "dst_host_same_srv_rate": "unusual service repetition to destination",
    "dst_host_diff_srv_rate": "destination contacted on many services",
    "dst_host_same_src_port_rate": "repeated use of same source port",
    "dst_host_srv_diff_host_rate": "service spread across many hosts",
    "dst_host_serror_rate": "high SYN errors at destination",
    "dst_host_srv_serror_rate": "high service SYN errors at destination",
    "dst_host_rerror_rate": "high REJ errors at destination",
    "dst_host_srv_rerror_rate": "high service REJ errors at destination"
}

MODEL_PATH = os.path.join("outputs", "model.pkl")


def train_model():
    """
    Trains Isolation Forest on NSL-KDD training data.
    Saves model to outputs/model.pkl.
    Returns the trained model.
    """
    from preprocessing import validate_and_preprocess

    print("Loading NSL-KDD training data...")
    with open(os.path.join("data", "KDDTrain+.txt"), "rb") as f:
        df, _ = validate_and_preprocess(f, "KDDTrain+.txt")

    print(f"Training Isolation Forest on {len(df)} records...")
    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42
    )
    model.fit(df)

    os.makedirs("outputs", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print(f"Model saved to {MODEL_PATH}")
    return model


def load_model():
    """
    Loads trained model from disk.
    Trains it first if it does not exist yet.
    """
    if not os.path.exists(MODEL_PATH):
        return train_model()

    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def get_risk_category(score):
    """
    Converts raw anomaly score to LOW / MEDIUM / HIGH.
    Isolation Forest scores: more negative = more anomalous.
    """
    if score < -0.15:
        return "HIGH"
    elif score < -0.05:
        return "MEDIUM"
    else:
        return "LOW"


def get_plain_english(top_features):
    """
    Converts top SHAP feature names into plain English sentences.
    """
    explanations = []
    for feature in top_features:
        if feature in FEATURE_TRANSLATIONS:
            explanations.append(FEATURE_TRANSLATIONS[feature])
        else:
            explanations.append(feature)
    return explanations


def run_scan(df):
    """
    Runs anomaly detection on a preprocessed DataFrame.
    Returns a list of flagged events with scores, risk category,
    plain English explanation, and top SHAP factors.
    """
    model = load_model()

    print("Generating anomaly scores...")
    scores = model.score_samples(df)
    predictions = model.predict(df)

    # Only flag records the model marks as anomalies (-1)
    flagged_indices = np.where(predictions == -1)[0]

    if len(flagged_indices) == 0:
        return []

    # Cap at top 500 most anomalous events to keep SHAP fast
    if len(flagged_indices) > 500:
        flagged_scores = scores[flagged_indices]
        top_500 = np.argsort(flagged_scores)[:500]
        flagged_indices = flagged_indices[top_500]

    print(f"Calculating SHAP values for {len(flagged_indices)} flagged events...")

    # Use a sample of background data for SHAP explainer
    background = shap.sample(df, 100, random_state=42)
    explainer = shap.Explainer(model.score_samples, background)

    flagged_df = df.iloc[flagged_indices]
    shap_values = explainer(flagged_df)

    flagged_events = []
    for i, idx in enumerate(flagged_indices):
        score = float(scores[idx])
        risk = get_risk_category(score)

        # Get top 3 features by absolute SHAP value
        shap_row = shap_values[i].values
        top_indices = np.argsort(np.abs(shap_row))[::-1][:3]
        top_features = [df.columns[j] for j in top_indices]
        plain_english_list = get_plain_english(top_features)

        flagged_events.append({
            "row_index": int(idx),
            "anomaly_score": score,
            "risk_category": risk,
            "top_factors": ",".join(plain_english_list),
            "plain_english": ". ".join(plain_english_list)
        })

    return flagged_events