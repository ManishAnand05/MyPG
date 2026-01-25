from fastapi import FastAPI
from app.routers import auth
from app.routers import pg 
from app.routers import room
from app.routers import bed
from app.routers import tenant
### Main Application File :- Initializes FastAPI app and includes routers .

app = FastAPI(title="MyPG Backend")

app.include_router(auth.router)
app.include_router(pg.router)
app.include_router(room.router)
app.include_router(bed.router)
app.include_router(tenant.router)

@app.get("/")
def root():
    return {"message": "MyPG backend running"}

# ### TODO: REMOVE after Alembic is added

# from app.core.database import Base, engine
# from app.models import (
#     user,
#     pg,
#     room,
#     bed,
#     tenant,
#     rent,
# )

# Base.metadata.create_all(bind=engine)
