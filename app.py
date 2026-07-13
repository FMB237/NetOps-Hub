from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return{
        "Hello Bro"
    }

@app.get('/Contact')
def Contact():
    return{"Welcome to the contact page "}
