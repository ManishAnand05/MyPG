from pydantic import BaseModel, EmailStr
from enum import Enum

### Pydantic Schemas for User :- Used for data validation and serialization

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    TENANT = "TENANT"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True
