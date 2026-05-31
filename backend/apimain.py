from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import joblib, numpy as np

from . import models, schemas, crud
from .database import SessionLocal, engine, Base

app = FastAPI(title="Diabetes Readmission API", version="2.0.0")

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load model + scaler
MODEL_PATH = Path("backend/ml/diabetes_model_rf.pkl")
SCALER_PATH = Path("backend/ml/diabetes_scaler.pkl")
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

@app.post("/patients")
def create_patient(record: schemas.PatientRecord, db: Session = Depends(get_db)):
    existing = crud.get_patient(db, record.patient_id)
    if existing:
        raise HTTPException(status_code=409, detail="Patient already exists")
    patient = crud.create_patient(db, record.patient_id, record.features.dict())
    return {"message": "Patient saved", "patient_id": patient.patient_id}

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient.__dict__

@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, updates: schemas.PatientUpdate, db: Session = Depends(get_db)):
    patient = crud.update_patient(db, patient_id, updates.dict(exclude_unset=True))
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "message": "Patient updated",
        "patient_id": patient_id,
        "updated_fields": updates.dict(exclude_unset=True)
    }

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = crud.delete_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": f"Patient {patient_id} and predictions deleted successfully"}

@app.post("/patients/{patient_id}/predict", response_model=schemas.PredictionOut)
def predict_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    features = {col: getattr(patient, col) for col in schemas.PatientFeatures.model_fields.keys()}
    X = np.array([[features[f] for f in features]], dtype=np.float64)
    Xs = scaler.transform(X)
    pred = int(model.predict(Xs)[0])
    proba = model.predict_proba(Xs)[0].tolist()

    result = {
        "prediction": pred,
        "probability_not_readmitted": round(proba[0], 4),
        "probability_readmitted": round(proba[1], 4),
        "confidence": round(max(proba), 4),
    }
    crud.save_prediction(db, patient_id, result)

    return schemas.PredictionOut(
        patient_id=patient_id,
        prediction=pred,
        prediction_label="Readmitted within 30 days" if pred == 1 else "Not readmitted within 30 days",
        probability_not_readmitted=result["probability_not_readmitted"],
        probability_readmitted=result["probability_readmitted"],
        confidence=result["confidence"],
        features_used=features
    )