from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def hello():
    return {'message': "hellow world"}

@app.get("/about")
def about():
    return {"message": "information python fastAPi"}