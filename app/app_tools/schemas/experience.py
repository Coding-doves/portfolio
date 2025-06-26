from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from app_tools.models.enums import LearningModeEnum


class ExperienceBase(BaseModel):
    role: str
    company: str
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None
    job_mode: Optional[LearningModeEnum] = None


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceOut(ExperienceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
