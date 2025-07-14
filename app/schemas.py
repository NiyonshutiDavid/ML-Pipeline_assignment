from pydantic import BaseModel

class PatientBase(BaseModel):
    name: str
    age: int
    sex: str
    resting_bp: float
    cholesterol: float
    fasting_bs: float
    max_hr: float
    exercise_angina: float
    oldpeak: float
    heart_disease: float
    st_slope_encoded: float
    resting_ecg_encoded: float
    chest_pain_asy: float
    chest_pain_ata: float
    chest_pain_nap: float
    chest_pain_ta: float

class PatientCreate(PatientBase):
    pass

class PatientOut(PatientBase):
    patient_id: int

    class Config:
        orm_mode = True
