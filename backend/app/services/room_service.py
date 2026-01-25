from sqlalchemy.orm import Session
from app.models.room import Room

def create_room(db: Session, room_number: int, pg_id: int):
    room = Room(room_number=room_number, pg_id=pg_id)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def get_rooms(db: Session, pg_id: int):
    return db.query(Room).filter(Room.pg_id == pg_id).all()
