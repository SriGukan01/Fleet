from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    APPLICANT = "applicant"
    OFFICER = "officer"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: str
    name: str
    role: UserRole = UserRole.APPLICANT
    organization: Optional[str] = None
    is_active: bool = True
    is_demo: bool = False

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str = Field(alias="_id")
    hashed_password: str
    created_at: str

    class Config:
        populate_by_name = True

class UserResponse(UserBase):
    id: str
    created_at: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class LoginRequest(BaseModel):
    email: str
    password: str

class DemoLoginRequest(BaseModel):
    role: UserRole
