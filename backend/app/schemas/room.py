from pydantic import BaseModel

class BedInRoom(BaseModel):
    id: int
    room_id: int
    rent: int
    is_occupied: bool

    class Config:
        from_attributes = True

class RoomCreate(BaseModel):
    pg_id: int
    room_number: int

class RoomResponse(BaseModel):
    id: int
    pg_id: int
    room_number: int
    beds: list[BedInRoom] = []

    class Config:
        from_attributes = True
