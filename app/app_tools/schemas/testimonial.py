from fastapi import File, UploadFile
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime


class TestimonialBase(BaseModel):
    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    message: str


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(TestimonialBase):
    pass


class TestimonialOut(TestimonialBase):
    id: int
    image: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
