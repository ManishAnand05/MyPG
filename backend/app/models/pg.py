from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class PG(Base):
    __tablename__ = "pgs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    rooms = relationship("Room", back_populates="pg", cascade="all, delete")
