from sqlalchemy.orm import Session
from app.models.room import Room
from fastapi import HTTPException

def create_room(db: Session, room_number: int, pg_id: int):
    room = Room(room_number=room_number, pg_id=pg_id)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def get_rooms(db: Session, pg_id: int):
    return db.query(Room).filter(Room.pg_id == pg_id).all()

def delete_room(db: Session, room_id: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Check if all beds are unoccupied
    occupied_beds = [bed for bed in room.beds if bed.is_occupied]
    if occupied_beds:
        raise HTTPException(status_code=400, detail="Cannot delete room with occupied beds")
    
    db.delete(room)
    db.commit()
    return {"message": "Room deleted successfully"}
