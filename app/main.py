from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import os

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

@app.post("/patients/", response_model=schemas.PatientOut)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

@app.get("/patients/", response_model=list[schemas.PatientOut])
def read_patients(db: Session = Depends(get_db)):
    return crud.get_patients(db)

@app.put("/patients/{patient_id}", response_model=schemas.PatientOut)
def update(patient_id: int, patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = crud.update_patient(db, patient_id, patient)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@app.delete("/patients/{patient_id}")
def delete(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.delete_patient(db, patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Deleted"}

@app.post("/predict/{patient_id}", response_model=schemas.PredictionResponse)
def predict_heart_disease(patient_id: int, db: Session = Depends(get_db)):
    """
    Predict heart disease for a specific patient using the trained Random Forest model
    """
    # 1) fetch patient
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # 2) load model
    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "models",
        "random_forest_model.pkl",
    )
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Model file not found")

    # 3) re‐apply training encodings
    sex_map    = {"M": 1, "F": 0}
    angina_map = {"Y": 1, "N": 0}

    sex_num    = sex_map   .get(patient.sex, 0)
    angina_num = angina_map.get(patient.exercise_angina, 0)

    # 4) build numeric feature vector
    features = np.array([[
        patient.age,
        sex_num,
        patient.resting_bp,
        patient.cholesterol,
        patient.fasting_bs,
        patient.max_hr,
        angina_num,
        patient.oldpeak,
        patient.st_slope_encoded,
        patient.resting_ecg_encoded,
        patient.chest_pain_asy,
        patient.chest_pain_ata,
        patient.chest_pain_nap,
        patient.chest_pain_ta,
    ]], dtype=float)

    # … after building `features` …
    print("⚙️  API received features:", features.tolist())

    prediction = model.predict(features)[0]

    # 5) predict
    prediction       = model.predict(features)[0]
    prediction_proba = model.predict_proba(features)[0]

    # 6) write back & return
    patient.heart_disease = float(prediction)
    db.commit()
    db.refresh(patient)

    return {
        "patient_id": patient_id,
        "patient_name": patient.name,
        "prediction": int(prediction),
        "prediction_text": "Heart Disease" if prediction == 1 else "No Heart Disease",
        "confidence": {
            "no_heart_disease": float(prediction_proba[0]),
            "heart_disease": float(prediction_proba[1]),
        },
        "features_used": {
            "age": patient.age,
            "sex": patient.sex,
            "resting_bp": patient.resting_bp,
            "cholesterol": patient.cholesterol,
            "fasting_bs": patient.fasting_bs,
            "max_hr": patient.max_hr,
            "exercise_angina": patient.exercise_angina,
            "oldpeak": patient.oldpeak,
            "st_slope_encoded": patient.st_slope_encoded,
            "resting_ecg_encoded": patient.resting_ecg_encoded,
            "chest_pain_asy": patient.chest_pain_asy,
            "chest_pain_ata": patient.chest_pain_ata,
            "chest_pain_nap": patient.chest_pain_nap,
            "chest_pain_ta": patient.chest_pain_ta,
        },
    }


@app.post("/predict-batch/", response_model=schemas.BatchPredictionResponse)
def predict_heart_disease_batch(db: Session = Depends(get_db)):
    """
    Predict heart disease for all patients in the database
    """
    patients = crud.get_patients(db)
    if not patients:
        raise HTTPException(status_code=404, detail="No patients found")

    model_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "models",
        "random_forest_model.pkl",
    )
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Model file not found")

    predictions = []
    sex_map    = {"M": 1, "F": 0}
    angina_map = {"Y": 1, "N": 0}

    for patient in patients:
        sex_num    = sex_map   .get(patient.sex, 0)
        angina_num = angina_map.get(patient.exercise_angina, 0)

        # build features
        features = np.array([[
            patient.age,
            sex_num,
            patient.resting_bp,
            patient.cholesterol,
            patient.fasting_bs,
            patient.max_hr,
            angina_num,
            patient.oldpeak,
            patient.st_slope_encoded,
            patient.resting_ecg_encoded,
            patient.chest_pain_asy,
            patient.chest_pain_ata,
            patient.chest_pain_nap,
            patient.chest_pain_ta,
        ]], dtype=float)

        prediction       = model.predict(features)[0]
        prediction_proba = model.predict_proba(features)[0]

        # append features_used exactly as single‐predict does
        predictions.append({
            "patient_id": patient.patient_id,
            "patient_name": patient.name,
            "prediction": int(prediction),
            "prediction_text": "Heart Disease" if prediction == 1 else "No Heart Disease",
            "confidence": {
                "no_heart_disease": float(prediction_proba[0]),
                "heart_disease":     float(prediction_proba[1]),
            },
            "features_used": {          # ← ← ← ADD THIS BLOCK
                "age":                patient.age,
                "sex":                patient.sex,
                "resting_bp":         patient.resting_bp,
                "cholesterol":        patient.cholesterol,
                "fasting_bs":         patient.fasting_bs,
                "max_hr":             patient.max_hr,
                "exercise_angina":    patient.exercise_angina,
                "oldpeak":            patient.oldpeak,
                "st_slope_encoded":   patient.st_slope_encoded,
                "resting_ecg_encoded":patient.resting_ecg_encoded,
                "chest_pain_asy":     patient.chest_pain_asy,
                "chest_pain_ata":     patient.chest_pain_ata,
                "chest_pain_nap":     patient.chest_pain_nap,
                "chest_pain_ta":      patient.chest_pain_ta,
            },
        })

        # persist the prediction value to the DB
        patient.heart_disease = float(prediction)

    db.commit()

    return {
        "total_patients": len(patients),
        "predictions":    predictions,
    }
