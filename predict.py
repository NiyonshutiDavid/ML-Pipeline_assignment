import requests
import numpy as np
import joblib
from app.database import SessionLocal
from app import models, schemas, crud

# Get latest patient
res = requests.get("http://localhost:8000/patients/")
latest = res.json()[-1]
X = np.array([[latest['age'], latest['sex'], latest['restingbp'], latest['cholesterol'], latest['fastingbs'], latest['maxhr'], latest['exerciseangina'], latest['oldpeak'], latest['st_slope_encoded'], latest['restingecg_encoded'], latest['chestpain_ASY'], latest['chestpain_ATA'], latest['chestpain_NAP'], latest['chestpain_TA']]])

# Predict
model = joblib.load('models/random_forest_model.pkl')
pred = model.predict(X)

# Add prediction to database
db = SessionLocal()
patient_db = crud.get_patient(db, latest['patient_id'])
patient_db.heartdisease = pred[0]
db.commit()

