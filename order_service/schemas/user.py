from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    login: str
    role: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    login: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    user_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True