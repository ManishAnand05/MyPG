from pydantic import BaseModel

class RoomCreate(BaseModel):
    pg_id: int
    room_number: int

class RoomResponse(BaseModel):
    id: int
    pg_id: int
    room_number: int

    class Config:
        orm_mode = True
