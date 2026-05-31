from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("http://127.0.0.1:5000/patients/new")  # Flask frontend URL

# Wait until the form is loaded
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "patient_id"))
)

# Fill Patient ID
driver.find_element(By.ID, "patient_id").send_keys("PT-20240001")

# Demographics
Select(driver.find_element(By.ID, "race")).select_by_value("2")
Select(driver.find_element(By.ID, "gender")).select_by_value("1")
Select(driver.find_element(By.ID, "Age_group")).select_by_value("5")

# Admission Info
driver.find_element(By.ID, "time_in_hospital").send_keys("3")
driver.find_element(By.ID, "payer_code").send_keys("1")
driver.find_element(By.ID, "medical_specialty").send_keys("10")

# Lab & Procedures
driver.find_element(By.ID, "num_lab_procedures").send_keys("41")
driver.find_element(By.ID, "num_procedures").send_keys("1")
driver.find_element(By.ID, "num_medications").send_keys("15")
driver.find_element(By.ID, "number_outpatient").send_keys("0")
driver.find_element(By.ID, "number_emergency").send_keys("0")
driver.find_element(By.ID, "number_inpatient").send_keys("1")

# Diagnoses
Select(driver.find_element(By.ID, "diag_1")).select_by_value("3")
Select(driver.find_element(By.ID, "diag_2")).select_by_value("0")
Select(driver.find_element(By.ID, "diag_3")).select_by_value("5")
driver.find_element(By.ID, "number_diagnoses").send_keys("7")

# Standard Medications
Select(driver.find_element(By.ID, "metformin")).select_by_value("1")
Select(driver.find_element(By.ID, "repaglinide")).select_by_value("0")
Select(driver.find_element(By.ID, "glimepiride")).select_by_value("0")
Select(driver.find_element(By.ID, "glipizide")).select_by_value("0")
Select(driver.find_element(By.ID, "glyburide")).select_by_value("0")
Select(driver.find_element(By.ID, "pioglitazone")).select_by_value("0")
Select(driver.find_element(By.ID, "rosiglitazone")).select_by_value("0")
Select(driver.find_element(By.ID, "insulin")).select_by_value("1")

# Binary Medications
Select(driver.find_element(By.ID, "nateglinide")).select_by_value("0")
Select(driver.find_element(By.ID, "chlorpropamide")).select_by_value("0")
Select(driver.find_element(By.ID, "acetohexamide")).select_by_value("0")
Select(driver.find_element(By.ID, "tolbutamide")).select_by_value("0")
Select(driver.find_element(By.ID, "acarbose")).select_by_value("0")
Select(driver.find_element(By.ID, "miglitol")).select_by_value("0")
Select(driver.find_element(By.ID, "troglitazone")).select_by_value("0")
Select(driver.find_element(By.ID, "tolazamide")).select_by_value("0")

# Combination Medications
Select(driver.find_element(By.ID, "glyburide_metformin")).select_by_value("0")
Select(driver.find_element(By.ID, "glipizide_metformin")).select_by_value("0")
Select(driver.find_element(By.ID, "glimepiride_pioglitazone")).select_by_value("0")
Select(driver.find_element(By.ID, "metformin_rosiglitazone")).select_by_value("0")
Select(driver.find_element(By.ID, "metformin_pioglitazone")).select_by_value("0")

# Medication Change & Diabetes Flag
Select(driver.find_element(By.ID, "change")).select_by_value("1")
Select(driver.find_element(By.ID, "diabetesMed")).select_by_value("1")

# Submit the form
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

print("✅ Form submitted successfully!")

driver.quit()