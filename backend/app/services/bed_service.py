from sqlalchemy.orm import Session
from app.models.bed import Bed

def create_bed(db: Session, rent, room_id: int):
    bed = Bed(rent=rent, room_id=room_id)
    db.add(bed)
    db.commit()
    db.refresh(bed)
    return bed

def get_beds(db: Session, room_id: int):
    return db.query(Bed).filter(Bed.room_id == room_id).all()
