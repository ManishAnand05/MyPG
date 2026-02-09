from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

### User Table Model

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    TENANT = "TENANT"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.TENANT)
    invited_pg_id = Column(Integer, ForeignKey("pgs.id"), nullable=True)
    invite_code = Column(String, nullable=True, index=True)
    
    pgs = relationship("PG", back_populates="admin", foreign_keys="[PG.admin_id]")
    invited_pg = relationship("PG", foreign_keys=[invited_pg_id])
    tenant_profile = relationship(
    "TenantProfile",
    back_populates="user",
    uselist=False
)


