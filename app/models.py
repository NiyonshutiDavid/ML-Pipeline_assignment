from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from .database import Base

class Patient(Base):
    __tablename__ = 'patients'
    patient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    sex = Column(String)
    resting_bp = Column(Float)
    cholesterol = Column(Float)
    fasting_bs = Column(Float)
    max_hr = Column(Float)
    exercise_angina = Column(Float)
    oldpeak = Column(Float)
    heart_disease = Column(Float)
    st_slope_encoded = Column(Float)
    resting_ecg_encoded = Column(Float)
    chest_pain_asy = Column(Float)
    chest_pain_ata = Column(Float)
    chest_pain_nap = Column(Float)
    chest_pain_ta = Column(Float)
