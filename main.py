from fastapi import FastAPI, Path, HTTPException, Query #the path() function is used to provide metadata, validation rules and documents hints for path parameters in API endpoints
#
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

@app.get("/patient/{id}")
def pathParams(id: str = Path(..., description="ID of the patient", example="P001")):
    data = load_data()
    if id in data:
        return data[id]
  
    return HTTPException(status_code=404, detail='Patient not found')

@app.get("/sort")
def sort_patient(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str = Query('asc', description="sort in asc or des order")):
    
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from{valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order select between asc and desc")
    
    data = load_data()

    sort_order = True if order == 'desc' else False

    sortedData = sorted(data.values(), key=lambda x:x.get(sort_by, 0), reverse=sort_order)

    return sortedData