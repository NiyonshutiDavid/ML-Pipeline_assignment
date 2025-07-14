# Heart Disease Prediction API

This project provides a FastAPI-based web service for predicting heart disease using a trained Random Forest model.

## Features

- **Patient Management**: Create, read, update, and delete patient records
- **Individual Prediction**: Predict heart disease for a specific patient
- **Batch Prediction**: Predict heart disease for all patients in the database
- **Confidence Scores**: Get prediction confidence levels

## API Endpoints

### Patient Management
- `POST /patients/` - Create a new patient
- `GET /patients/` - Get all patients
- `PUT /patients/{patient_id}` - Update a patient
- `DELETE /patients/{patient_id}` - Delete a patient

### Prediction Endpoints
- `POST /predict/{patient_id}` - Predict heart disease for a specific patient
- `POST /predict-batch/` - Predict heart disease for all patients

## Required Patient Data

When creating a patient, provide the following features:
- `name`: Patient name (string)
- `age`: Age in years (integer)
- `sex`: Gender (1 for male, 0 for female)
- `resting_bp`: Resting blood pressure (float)
- `cholesterol`: Cholesterol level (float)
- `fasting_bs`: Fasting blood sugar (float)
- `max_hr`: Maximum heart rate (float)
- `exercise_angina`: Exercise-induced angina (float)
- `oldpeak`: ST depression (float)
- `st_slope_encoded`: Encoded ST slope (float)
- `resting_ecg_encoded`: Encoded resting ECG (float)
- `chest_pain_asy`: Asymptomatic chest pain (float)
- `chest_pain_ata`: Atypical angina chest pain (float)
- `chest_pain_nap`: Non-anginal pain (float)
- `chest_pain_ta`: Typical angina chest pain (float)

## Usage

### 1. Start the Server
```bash
cd /home/rurangwa/Dev/ALU/ML/ML-Pipeline_assignment
uvicorn app.main:app --reload
```

### 2. Create a Patient
```bash
curl -X POST "http://localhost:8000/patients/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "age": 45,
       "sex": 1,
       "resting_bp": 130.0,
       "cholesterol": 250.0,
       "fasting_bs": 0.0,
       "max_hr": 150.0,
       "exercise_angina": 0.0,
       "oldpeak": 1.2,
       "heart_disease": 0.0,
       "st_slope_encoded": 2.0,
       "resting_ecg_encoded": 1.0,
       "chest_pain_asy": 1.0,
       "chest_pain_ata": 0.0,
       "chest_pain_nap": 0.0,
       "chest_pain_ta": 0.0
     }'
```

### 3. Predict Heart Disease
```bash
# For a specific patient (replace 1 with actual patient_id)
curl -X POST "http://localhost:8000/predict/1"

# For all patients
curl -X POST "http://localhost:8000/predict-batch/"
```

### 4. Test with the Provided Script
```bash
python test_prediction.py
```

## Prediction Response

The prediction endpoints return:
- `patient_id`: Patient identifier
- `patient_name`: Patient name
- `prediction`: 0 (No Heart Disease) or 1 (Heart Disease)
- `prediction_text`: Human-readable prediction
- `confidence`: Confidence scores for both classes
- `features_used`: The features used for prediction (individual endpoint only)

## Example Response

```json
{
  "patient_id": 1,
  "patient_name": "John Doe",
  "prediction": 1,
  "prediction_text": "Heart Disease",
  "confidence": {
    "no_heart_disease": 0.3,
    "heart_disease": 0.7
  },
  "features_used": {
    "age": 45,
    "sex": 1,
    "resting_bp": 130.0,
    ...
  }
}
```

## Model

The system uses a pre-trained Random Forest model located in `models/random_forest_model.pkl`. The model was trained on heart disease data and expects 14 features for prediction.

## Database

Patient data is stored in an SQLite database. The database schema is automatically created when the application starts.
