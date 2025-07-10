-- File: sql/schema.sql

CREATE TABLE Patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    cholesterol FLOAT,
    blood_pressure FLOAT
);

CREATE TABLE Doctors (
    doctor_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    specialty VARCHAR(100)
);

CREATE TABLE Diagnoses (
    diagnosis_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES Patients(patient_id),
    doctor_id INT REFERENCES Doctors(doctor_id),
    heart_disease BOOLEAN,
    date DATE DEFAULT CURRENT_DATE
);

-- Stored Procedure: Check for high cholesterol
CREATE OR REPLACE FUNCTION validate_cholesterol()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.cholesterol > 250 THEN
    RAISE NOTICE 'High cholesterol detected!';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER cholesterol_trigger
BEFORE INSERT ON Patients
FOR EACH ROW EXECUTE FUNCTION validate_cholesterol();
