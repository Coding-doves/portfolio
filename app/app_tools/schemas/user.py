from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    name: str
    email: EmailStr


class UserCreate(User):
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: Optional[datetime] = None
    is_active: bool
    is_verified: bool


class UserLogin(User):
    pass


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: Optional[datetime] = None
    message: str = "Login successful"
    user: dict = None
