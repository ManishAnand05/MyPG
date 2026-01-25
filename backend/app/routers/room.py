from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.room import RoomCreate, RoomResponse
from app.services.room_service import create_room, get_rooms

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/", response_model=RoomResponse)
def add_room(room: RoomCreate, db: Session = Depends(get_db)):
    return create_room(db, room.room_number, room.pg_id)

@router.get("/{pg_id}", response_model=list[RoomResponse])
def list_rooms(pg_id: int, db: Session = Depends(get_db)):
    return get_rooms(db, pg_id)
