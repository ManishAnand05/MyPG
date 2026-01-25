from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Bed(Base):
    __tablename__ = "beds"

    id = Column(Integer, primary_key=True, index=True)
    rent = Column(Integer, nullable=False)
    is_occupied = Column(Boolean, default=False)

    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)

    room = relationship("Room", back_populates="beds")
    tenant = relationship("TenantProfile", back_populates="bed", uselist=False)
