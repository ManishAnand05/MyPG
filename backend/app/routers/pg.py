from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.pg import PGCreate, PGResponse
from app.services.pg_service import create_pg, get_pgs

router = APIRouter(prefix="/pg", tags=["PG"])

@router.post("/", response_model=PGResponse)
def add_pg(pg: PGCreate, db: Session = Depends(get_db)):
    return create_pg(db, pg.name, pg.location)

@router.get("/", response_model=list[PGResponse])
def list_pgs(db: Session = Depends(get_db)):
    return get_pgs(db)
