from fastapi import FastAPI 

import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f: #reading json file
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {'message': "patient management system api"}

@app.get("/about")
def about():
    return {"message": "manage patients records"}

@app.get('/view')
def view():
    data = load_data()

    return data