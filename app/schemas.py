from pydantic import BaseModel

class PatientBase(BaseModel):
    name: str
    Age: int
    Sex: str
    RestingBP: float
    Cholesterol: float
    FastingBS: float
    MaxHR: float
    ExerciseAngina: float
    Oldpeak: float
    HeartDisease: float
    ST_Slope_encoded: float
    RestingECG_encoded: float
    ChestPain_ASY: float
    ChestPain_ATA: float
    ChestPain_NAP: float
    ChestPain_TA: float

class PatientCreate(PatientBase):
    pass

class PatientOut(PatientBase):
    patient_id: int

    class Config:
        orm_mode = True
