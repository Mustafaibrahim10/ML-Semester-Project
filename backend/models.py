from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(String(64), primary_key=True, index=True)
    # 39 features as columns
    race = Column(Integer)
    gender = Column(Integer)
    Age_group = Column(Integer)
    time_in_hospital = Column(Integer)
    payer_code = Column(Integer)
    medical_specialty = Column(Integer)
    num_lab_procedures = Column(Integer)
    num_procedures = Column(Integer)
    num_medications = Column(Integer)
    number_outpatient = Column(Integer)
    number_emergency = Column(Integer)
    number_inpatient = Column(Integer)
    diag_1 = Column(Integer)
    diag_2 = Column(Integer)
    diag_3 = Column(Integer)
    number_diagnoses = Column(Integer)
    metformin = Column(Integer)
    repaglinide = Column(Integer)
    nateglinide = Column(Integer)
    chlorpropamide = Column(Integer)
    glimepiride = Column(Integer)
    acetohexamide = Column(Integer)
    glipizide = Column(Integer)
    glyburide = Column(Integer)
    tolbutamide = Column(Integer)
    pioglitazone = Column(Integer)
    rosiglitazone = Column(Integer)
    acarbose = Column(Integer)
    miglitol = Column(Integer)
    troglitazone = Column(Integer)
    tolazamide = Column(Integer)
    insulin = Column(Integer)
    glyburide_metformin = Column(Integer)
    glipizide_metformin = Column(Integer)
    glimepiride_pioglitazone = Column(Integer)
    metformin_rosiglitazone = Column(Integer)
    metformin_pioglitazone = Column(Integer)
    change = Column(Integer)
    diabetesMed = Column(Integer)

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(64), ForeignKey("patients.patient_id"))
    prediction = Column(Integer)
    probability_not_readmitted = Column(Float)
    probability_readmitted = Column(Float)
    confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())