import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class RentStatus(str, enum.Enum):
    PAID = "PAID"
    DUE = "DUE"

class Rent(Base):
    __tablename__ = "rents"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    month = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(Enum(RentStatus), default=RentStatus.DUE)
    tenant = relationship("TenantProfile", back_populates="rents")
