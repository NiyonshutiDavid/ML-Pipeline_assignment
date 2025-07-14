import sys
import os
import requests
import numpy as np
import joblib
from app.database import SessionLocal
from app import crud

# 0) Determine base URL / port
if len(sys.argv) > 1:
    port = sys.argv[1]
else:
    port = os.getenv("API_PORT", "8000")

BASE_URL = f"http://localhost:{port}"

# 1) Fetch the latest patient record
res = requests.get(f"{BASE_URL}/patients/")
res.raise_for_status()
latest = res.json()[-1]

patient_name = latest['name']


# 2) Reproduce your training encodings for sex
sex_map = {"M": 1, "F": 0}

# 3) Build your numeric feature vector using the correct snake_case keys
X = np.array([[
    latest['age'],
    sex_map[latest['sex']],           # map M/F → 1/0
    latest['resting_bp'],             # was restingbp
    latest['cholesterol'],
    latest['fasting_bs'],             # was fastingbs
    latest['max_hr'],                 # was maxhr
    latest['exercise_angina'],        # stored as 0.0/1.0 already
    latest['oldpeak'],
    latest['st_slope_encoded'],
    latest['resting_ecg_encoded'],
    latest['chest_pain_asy'],         # was chestpain_ASY
    latest['chest_pain_ata'],         # was chestpain_ATA
    latest['chest_pain_nap'],         # was chestpain_NAP
    latest['chest_pain_ta'],          # was chestpain_TA
]], dtype=float)

# … after building latest and X …

print("🔍 Raw JSON from API:", latest)
print("🔢 Feature vector X:", X.tolist())


# 4) Load & predict
model = joblib.load('models/random_forest_model.pkl')
pred   = model.predict(X)[0]

# 5) Write back to your DB (underscore in attribute name)
db = SessionLocal()
patient_db = crud.get_patient(db, latest['patient_id'])
patient_db.heart_disease = float(pred)
db.commit()

print(
    f"Predicted {pred} for patient {latest['patient_id']} "
    f"({patient_name}) on port {port}"
)