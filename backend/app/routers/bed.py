from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.bed import BedCreate, BedResponse
from app.services.bed_service import create_bed, get_beds, delete_bed, get_available_beds_grouped

router = APIRouter(prefix="/beds", tags=["Beds"])

@router.get("/available")
def list_available_beds(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_available_beds_grouped(db, current_user)

@router.post("/create", response_model=BedResponse)
def add_bed(bed: BedCreate, db: Session = Depends(get_db)):
    return create_bed(db, bed.rent, bed.room_id)

@router.get("/{room_id}", response_model=list[BedResponse])
def list_beds(room_id: int, db: Session = Depends(get_db)):
    return get_beds(db, room_id)

@router.delete("/{bed_id}")
def remove_bed(bed_id: int, db: Session = Depends(get_db)):
    return delete_bed(db, bed_id)
