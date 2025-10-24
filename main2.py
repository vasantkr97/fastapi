
from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title="Name of the patient", description="Give patient name less than 50 char", examples=['vasanth', "maneri"])]
    email: EmailStr
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=False, description='is the patient married or not')]
    allergies: Optional[List[str]] = Field(max_length=5)
    contact_details: Dict[str, str]


def insert(patient: Patient):
    print(patient.name)
    print(patient.age)


patient_info = {"name": "vasanth","email":"abc@gamil.com", "age": 23, "weight": 62.0, "married": False,"allergies": ['pollen', 'dust'], "contact_details": {"email": "casdas2gmail.com", 'phone': "2345325345234"}}

patient1 = Patient(**patient_info)

insert(patient1)

















# from pydantic import BaseModel


# class Patient(BaseModel):
#     name: str 
#     age: int 

# def insert(patient: Patient):
#     print(patient.name)
#     print(patient.age)



# patient_info = { "name": 'vasanth', 'age': 23}

# patient1 = Patient(**patient_info)

# insert(patient1)




# def insert_patient_data(name:str, age: int):

#     if type(name) == str and type(age) == int:
#         print(name)
#         print(age)
#     else:
#         raise TypeError("Incoorect data type")
# insert_patient_data("vasanth", "23")           