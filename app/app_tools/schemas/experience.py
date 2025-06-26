from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ExperienceBase(BaseModel):
    role: str
    company: str
    location: Optional[str]
    start_date: date
    end_date: Optional[date]
    description: Optional[str]


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceOut(ExperienceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
