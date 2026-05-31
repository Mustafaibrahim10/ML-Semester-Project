import numpy as np
from pydantic import BaseModel, Field
from typing import Dict, Optional

FEATURE_COLUMNS = [
    "race", "gender", "time_in_hospital", "payer_code", "medical_specialty",
    "num_lab_procedures", "num_procedures", "num_medications",
    "number_outpatient", "number_emergency", "number_inpatient",
    "diag_1", "diag_2", "diag_3", "number_diagnoses",
    "metformin", "repaglinide", "nateglinide", "chlorpropamide",
    "glimepiride", "acetohexamide", "glipizide", "glyburide", "tolbutamide",
    "pioglitazone", "rosiglitazone", "acarbose", "miglitol", "troglitazone",
    "tolazamide", "insulin",
    "glyburide-metformin", "glipizide-metformin", "glimepiride-pioglitazone",
    "metformin-rosiglitazone", "metformin-pioglitazone",
    "change", "diabetesMed", "Age_group",
]

RACE_LABELS  = {0: "AfricanAmerican", 1: "Asian", 2: "Caucasian", 3: "Hispanic", 4: "Other"}
GENDER_LABELS = {0: "Female", 1: "Male"}
DIAG_LABELS  = {
    0: "Circulatory", 1: "Respiratory", 2: "Digestive", 3: "Diabetes",
    4: "Injury", 5: "Musculoskeletal", 6: "Genitourinary", 7: "Neoplasms", 8: "Other",
}

class PatientFeatures(BaseModel):
    """
    All 39 model features — every field is required and validated.
    """
    race:              int = Field(..., ge=0, le=4,   description="0=AfricanAmerican 1=Asian 2=Caucasian 3=Hispanic 4=Other")
    gender:            int = Field(..., ge=0, le=1,   description="0=Female 1=Male")
    Age_group:         int = Field(..., ge=0, le=9,   description="0=[0-10) … 9=[90-100)")
    time_in_hospital:  int = Field(..., ge=1, le=14)
    payer_code:        int = Field(..., ge=0, le=13)
    medical_specialty: int = Field(..., ge=0, le=48)
    num_lab_procedures:int = Field(..., ge=1, le=132)
    num_procedures:    int = Field(..., ge=0, le=6)
    num_medications:   int = Field(..., ge=1, le=81)
    number_outpatient: int = Field(..., ge=0, le=42)
    number_emergency:  int = Field(..., ge=0, le=76)
    number_inpatient:  int = Field(..., ge=0, le=21)
    diag_1:            int = Field(..., ge=0, le=8)
    diag_2:            int = Field(..., ge=0, le=8)
    diag_3:            int = Field(..., ge=0, le=8)
    number_diagnoses:  int = Field(..., ge=1, le=16)
    metformin:         int = Field(..., ge=0, le=3)
    repaglinide:       int = Field(..., ge=0, le=3)
    nateglinide:       int = Field(..., ge=0, le=1)
    chlorpropamide:    int = Field(..., ge=0, le=1)
    glimepiride:       int = Field(..., ge=0, le=3)
    acetohexamide:     int = Field(..., ge=0, le=1)
    glipizide:         int = Field(..., ge=0, le=3)
    glyburide:         int = Field(..., ge=0, le=3)
    tolbutamide:       int = Field(..., ge=0, le=1)
    pioglitazone:      int = Field(..., ge=0, le=3)
    rosiglitazone:     int = Field(..., ge=0, le=3)
    acarbose:          int = Field(..., ge=0, le=1)
    miglitol:          int = Field(..., ge=0, le=1)
    troglitazone:      int = Field(..., ge=0, le=1)
    tolazamide:        int = Field(..., ge=0, le=1)
    insulin:           int = Field(..., ge=0, le=3)
    glyburide_metformin:        int = Field(..., ge=0, le=1, alias="glyburide-metformin")
    glipizide_metformin:        int = Field(..., ge=0, le=1, alias="glipizide-metformin")
    glimepiride_pioglitazone:   int = Field(..., ge=0, le=1, alias="glimepiride-pioglitazone")
    metformin_rosiglitazone:    int = Field(..., ge=0, le=1, alias="metformin-rosiglitazone")
    metformin_pioglitazone:     int = Field(..., ge=0, le=1, alias="metformin-pioglitazone")
    change:      int = Field(..., ge=0, le=1)
    diabetesMed: int = Field(..., ge=0, le=1)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "race": 2, "gender": 1, "Age_group": 5,
                "time_in_hospital": 3, "payer_code": 1, "medical_specialty": 10,
                "num_lab_procedures": 41, "num_procedures": 1, "num_medications": 15,
                "number_outpatient": 0, "number_emergency": 0, "number_inpatient": 1,
                "diag_1": 3, "diag_2": 0, "diag_3": 5, "number_diagnoses": 7,
                "metformin": 1, "repaglinide": 0, "nateglinide": 0,
                "chlorpropamide": 0, "glimepiride": 0, "acetohexamide": 0,
                "glipizide": 0, "glyburide": 0, "tolbutamide": 0,
                "pioglitazone": 0, "rosiglitazone": 0, "acarbose": 0,
                "miglitol": 0, "troglitazone": 0, "tolazamide": 0, "insulin": 1,
                "glyburide-metformin": 0, "glipizide-metformin": 0,
                "glimepiride-pioglitazone": 0, "metformin-rosiglitazone": 0,
                "metformin-pioglitazone": 0,
                "change": 1, "diabetesMed": 1,
            }
        },
    }

    def to_feature_dict(self) -> dict:
        """Flat dict with original hyphenated column names (alias keys)."""
        return self.model_dump(by_alias=True)

    def to_feature_array(self) -> np.ndarray:
        d = self.to_feature_dict()
        return np.array([[d[col] for col in FEATURE_COLUMNS]], dtype=np.float64)

class PatientRecord(BaseModel):
    patient_id: str
    features: PatientFeatures

class PatientUpdate(BaseModel):
    # All fields optional for partial updates
    race: Optional[int] = None
    gender: Optional[int] = None
    Age_group: Optional[int] = None
    time_in_hospital: Optional[int] = None
    payer_code: Optional[int] = None
    medical_specialty: Optional[int] = None
    num_lab_procedures: Optional[int] = None
    num_procedures: Optional[int] = None
    num_medications: Optional[int] = None
    number_outpatient: Optional[int] = None
    number_emergency: Optional[int] = None
    number_inpatient: Optional[int] = None
    diag_1: Optional[int] = None
    diag_2: Optional[int] = None
    diag_3: Optional[int] = None
    number_diagnoses: Optional[int] = None
    metformin: Optional[int] = None
    repaglinide: Optional[int] = None
    nateglinide: Optional[int] = None
    chlorpropamide: Optional[int] = None
    glimepiride: Optional[int] = None
    acetohexamide: Optional[int] = None
    glipizide: Optional[int] = None
    glyburide: Optional[int] = None
    tolbutamide: Optional[int] = None
    pioglitazone: Optional[int] = None
    rosiglitazone: Optional[int] = None
    acarbose: Optional[int] = None
    miglitol: Optional[int] = None
    troglitazone: Optional[int] = None
    tolazamide: Optional[int] = None
    insulin: Optional[int] = None
    glyburide_metformin: Optional[int] = None
    glipizide_metformin: Optional[int] = None
    glimepiride_pioglitazone: Optional[int] = None
    metformin_rosiglitazone: Optional[int] = None
    metformin_pioglitazone: Optional[int] = None
    change: Optional[int] = None
    diabetesMed: Optional[int] = None

class PredictionOut(BaseModel):
    patient_id: str
    prediction: int
    prediction_label: str
    probability_not_readmitted: float
    probability_readmitted: float
    confidence: float
    features_used: Dict[str, int]