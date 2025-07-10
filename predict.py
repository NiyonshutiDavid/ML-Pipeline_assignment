import requests
import numpy as np
import joblib

# Get latest patient
res = requests.get("http://localhost:8000/patients/")
latest = res.json()[-1]
X = np.array([[latest['age'], latest['cholesterol'], latest['blood_pressure']]])

# Predict
model = joblib.load('model/heart_model.pkl')
pred = model.predict(X)
print(f"Prediction for {latest['name']}: {'Heart Disease' if pred[0] else 'No Heart Disease'}")
