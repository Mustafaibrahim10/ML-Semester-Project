from sqlalchemy.orm import Session
from . import models

def get_patient(db: Session, patient_id: str):
    return db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()

def create_patient(db: Session, patient_id: str, features: dict):
    patient = models.Patient(patient_id=patient_id, **features)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def update_patient(db: Session, patient_id: str, updates: dict):
    patient = get_patient(db, patient_id)
    if not patient:
        return None
    for key, value in updates.items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    return patient

def delete_patient(db: Session, patient_id: str):
    patient = get_patient(db, patient_id)
    if not patient:
        return None
    # Delete predictions linked to this patient
    db.query(models.Prediction).filter(models.Prediction.patient_id == patient_id).delete()
    db.delete(patient)
    db.commit()
    return patient

def save_prediction(db: Session, patient_id: str, result: dict):
    prediction = models.Prediction(patient_id=patient_id, **result)
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction