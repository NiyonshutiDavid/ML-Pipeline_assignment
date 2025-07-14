-- File: schema.sql
DROP TABLE IF EXISTS diagnoses CASCADE; -- CASCADE is important if other objects depend on it (like foreign keys)
DROP TABLE IF EXISTS doctors CASCADE;
DROP TABLE IF EXISTS patients CASCADE;

-- Also drop the trigger if it exists before recreating it
DROP TRIGGER IF EXISTS cholesterol_trigger ON patients;
DROP FUNCTION IF EXISTS calculate_cholesterol_status();

CREATE TABLE Patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    sex VARCHAR(10),
    restingbp FLOAT,
    cholesterol FLOAT,
    fastingbs FLOAT,
    maxhr FLOAT,
    exerciseangina FLOAT,
    oldpeak FLOAT,
    heartdisease FLOAT,
    st_slope_encoded FLOAT,
    restingecg_encoded FLOAT,
    chestpain_ASY FLOAT,
    chestpain_ATA FLOAT,
    chestpain_NAP FLOAT,
    chestpain_TA FLOAT
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
-- Popularize database with data from cleaned dataset --
\copy Patients(Age, Sex, RestingBP, Cholesterol, FastingBS, MaxHR, ExerciseAngina, Oldpeak, HeartDisease, ST_Slope_encoded, RestingECG_encoded, ChestPain_ASY, ChestPain_ATA, ChestPain_NAP, ChestPain_TA) FROM 'data/heart_cleaned.csv' CSV HEADER;