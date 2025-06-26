from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class TestimonialBase(BaseModel):
    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    message: str
    image: Optional[str] = None  # can be file path or URL

class TestimonialCreate(TestimonialBase):
    pass

class TestimonialUpdate(TestimonialBase):
    pass

class TestimonialOut(TestimonialBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
