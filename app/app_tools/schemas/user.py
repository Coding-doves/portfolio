from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRole(str, Enum):
    root = "root"
    admin = "admin"


class ProfileBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    profile_image: Optional[str]
    resume_link: Optional[str]


class ProfileCreate(ProfileBase):
    pass


class ProfileOut(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(BaseModel):
    name: str
    email: EmailStr


class UserCreate(User):
    password: str
    role: Optional[UserRole] = UserRole.admin


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    created_at: Optional[datetime] = None
    is_active: bool
    is_verified: bool
    profile: Optional[ProfileOut]

    class Config:
        from_attributes = True


class UserLogin(User):
    pass


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: Optional[datetime] = None
    message: str = "Login successful"
    user: dict = None
