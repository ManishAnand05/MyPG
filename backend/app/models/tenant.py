from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class TenantProfile(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    bed_id = Column(Integer, ForeignKey("beds.id"), nullable=False, unique=True)

    move_in_date = Column(Date, nullable=False)

    bed = relationship("Bed", back_populates="tenant")
