from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json, os

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient is from")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['male', 'female','others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of patient in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of patient in kilograms")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    gender: Optional[Literal['male', 'female','others']] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)

    @computed_field
    @property
    def bmi(self) -> Optional[float]:
        if self.height is None or self.weight is None:
            return None
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> Optional[str]:
        if self.bmi is None:
            return None
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

def load_data():
    if not os.path.exists("patients.json"):
        return {}
    with open("patients.json", "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)

@app.post('/create')
def createPatient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=201, content={
        "message": "Patient created successfully",
        "patient": patient.model_dump()
    })

@app.put("/update/{id}")
def updateDetails(id: str, patient_update: PatientUpdate):
    data = load_data()
    if id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_info = data[id]
    updatedPatientDict = patient_update.model_dump(exclude_unset=True)

    for key, value in updatedPatientDict.items():
        patient_info[key] = value

    patient_info["id"] = id
    patient_pydantic_ob = Patient(**patient_info)
    data[id] = patient_pydantic_ob.model_dump(exclude=['id'])
    
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

@app.get('/allpatients')
def allpatients():
    return load_data()
