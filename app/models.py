from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from .database import Base

class Patient(Base):
    __tablename__ = 'patients'
    patient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    cholesterol = Column(Float)
    blood_pressure = Column(Float)
