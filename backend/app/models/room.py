from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(Integer, nullable=False)

    pg_id = Column(Integer, ForeignKey("pgs.id"), nullable=False)

    pg = relationship("PG", back_populates="rooms")
    beds = relationship("Bed", back_populates="room", cascade="all, delete")
