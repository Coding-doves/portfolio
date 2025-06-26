from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from app_tools.models.enums import LearningModeEnum


class EducationBase(BaseModel):
    degree: str
    course: Optional[str] = None
    institution: str
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None
    learning_mode: Optional[LearningModeEnum] = None


class EducationCreate(EducationBase):
    pass


class EducationOut(EducationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
