from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="MyPG Backend")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "MyPG backend running"}


