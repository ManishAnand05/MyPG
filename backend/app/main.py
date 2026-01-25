from fastapi import FastAPI
from app.routers import auth
from app.routers import pg 
### Main Application File :- Initializes FastAPI app and includes routers .

app = FastAPI(title="MyPG Backend")

app.include_router(auth.router)
app.include_router(pg.router)

@app.get("/")
def root():
    return {"message": "MyPG backend running"}


