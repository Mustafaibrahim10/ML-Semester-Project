import requests

BASE_URL = "http://127.0.0.1:8000"  # FastAPI backend

# Example patient payload (matches PatientFeatures schema)
patient_data = {
    "patient_id": '003',
    "features": {
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
        "change": 1, "diabetesMed": 1
    }
}

def test_create_patient():
    r = requests.post(f"{BASE_URL}/patients/", json=patient_data)
    print("Create:", r.status_code, r.json())

def test_read_patient(patient_id='003'):
    r = requests.get(f"{BASE_URL}/patients/{patient_id}")
    print("Read:", r.status_code, r.json())

def test_update_patient(patient_id='003'):
    update = {"num_medications": 20}
    r = requests.put(f"{BASE_URL}/patients/{patient_id}", json=update)
    print("Update:", r.status_code, r.json())

def test_delete_patient(patient_id='003'):
    r = requests.delete(f"{BASE_URL}/patients/{patient_id}")
    print("Delete:", r.status_code)

def test_predict(patient_id='003'):
    r = requests.post(f"{BASE_URL}/patients/{patient_id}/predict")
    print("Predict:", r.status_code, r.json())

if __name__ == "__main__":
    #test_create_patient()
    test_read_patient()
    test_update_patient()
    test_predict()
    #test_delete_patient()