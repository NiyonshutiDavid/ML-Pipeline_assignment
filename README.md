# Heart Disease Prediction & Patient Management API

This project is a machine learning–powered API for predicting heart disease and managing patient records. It includes:

- A trained Random Forest model for heart disease prediction
- A FastAPI backend with full CRUD operations on patient data
- Relational database integration (e.g., SQLite or PostgreSQL)
- Preprocessing script and model inference capabilities

---

## Project Structure

```
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── database.py
├── data/
├── heart_cleaned.csv
├── Notebook.ipynb
├── train_model.py
├── predict.py
├── random_forest_model.pkl
├── schema.sql
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/NiyonshutiDavid/ML-Pipeline_assignment.git
```
```bash
cd ML-Pipeline_assignment
```
2. Install dependencies

```bash
pip install -r requirements.txt
```
3. Start the API

```bash
uvicorn app.main:app --reload
```
Visit: http://localhost:8000/docs to explore the auto-generated Swagger UI.

API Endpoints
```
Method	Endpoint	Description
POST	/patients/	Create a new patient
GET	/patients/	Get all patients
GET	/patients/{id}	Get a patient by ID
PUT	/patients/{id}	Update a patient by ID
DELETE	/patients/{id}	Delete a patient by ID
```
All endpoints operate on the SQL database defined in app/database.py.

Machine Learning

    Dataset: heart_cleaned.csv

    Model: Random Forest Classifier

    Trained model file: random_forest_model.pkl

    Use predict.py to load the model and make predictions on new patient data.

## 🧑‍🤝‍🧑 Team Contributions
```
Member	/Role
Prince Rurangwa /- CRUD Operations and API
David Niyonshuti /- Database schema & report
Anne Marie Twagirayezu /- Model training & prediction script
Chol Daniel Deng Dau /- Data Cleaning and preprocessing (data preparation for using)
```
📎 Additional Files

    schema.sql – SQL file with relational schema (≥ 3 tables with PKs + FKs)

    ERD Diagram 
