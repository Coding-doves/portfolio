from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class ContactMessageBase(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str]
    message: str


class ContactMessageCreate(ContactMessageBase):
    pass


class ContactMessageOut(ContactMessageBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
