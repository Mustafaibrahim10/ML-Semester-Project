from pathlib import Path
import joblib
import numpy as np

MODEL_PATH = Path("backend/ml/diabetes_model_rf.pkl")
SCALER_PATH = Path("backend/ml/diabetes_scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def preprocess(features: dict, feature_order: list) -> np.ndarray:
    X = np.array([[features[col] for col in feature_order]], dtype=np.float64)
    return scaler.transform(X)

def predict(features: dict, feature_order: list) -> dict:
    Xs = preprocess(features, feature_order)
    pred = int(model.predict(Xs)[0])
    proba = model.predict_proba(Xs)[0].tolist()

    return {
        "prediction": pred,
        "prediction_label": "Readmitted within 30 days" if pred == 1 else "Not readmitted within 30 days",
        "probability_not_readmitted": round(proba[0], 4),
        "probability_readmitted": round(proba[1], 4),
        "confidence": round(max(proba), 4),
    }