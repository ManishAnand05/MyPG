from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.bed import BedCreate, BedResponse
from app.services.bed_service import create_bed, get_beds

router = APIRouter(prefix="/beds", tags=["Beds"])

@router.post("/", response_model=BedResponse)
def add_bed(bed: BedCreate, db: Session = Depends(get_db)):
    return create_bed(db, bed.bed_number, bed.room_id)

@router.get("/{room_id}", response_model=list[BedResponse])
def list_beds(room_id: int, db: Session = Depends(get_db)):
    return get_beds(db, room_id)
