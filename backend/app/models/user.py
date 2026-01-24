from sqlalchemy import Column, Integer, String, Enum
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    TENANT = "TENANT"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.ADMIN)


