from sqlalchemy.orm import Session
from app.models.bed import Bed
from fastapi import HTTPException

def create_bed(db: Session, rent, room_id: int):
    bed = Bed(rent=rent, room_id=room_id)
    db.add(bed)
    db.commit()
    db.refresh(bed)
    return bed

def get_beds(db: Session, room_id: int):
    return db.query(Bed).filter(Bed.room_id == room_id).all()

def delete_bed(db: Session, bed_id: int):
    bed = db.query(Bed).filter(Bed.id == bed_id).first()
    if not bed:
        raise HTTPException(status_code=404, detail="Bed not found")
    
    if bed.is_occupied:
        raise HTTPException(status_code=400, detail="Cannot delete an occupied bed")
    
    db.delete(bed)
    db.commit()
    return {"message": "Bed deleted successfully"}
