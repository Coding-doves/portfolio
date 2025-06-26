from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class EducationBase(BaseModel):
    degree: str
    institution: str
    location: Optional[str]
    start_date: date
    end_date: Optional[date]
    description: Optional[str]


class EducationCreate(EducationBase):
    pass


class EducationOut(EducationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
