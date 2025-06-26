from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --- Skill Category ---
class SkillCategoryBase(BaseModel):
    name: str
    slug: Optional[str]


class SkillCategoryCreate(SkillCategoryBase):
    pass


class SkillCategoryOut(SkillCategoryBase):
    id: int

    class Config:
        from_attributes = True


# --- Skill ---
class SkillBase(BaseModel):
    name: str
    proficiency: Optional[str]
    icon: Optional[str]
    category_id: Optional[int]


class SkillCreate(SkillBase):
    pass


class SkillOut(SkillBase):
    id: int
    created_at: datetime
    category: Optional[SkillCategoryOut]

    class Config:
        from_attributes = True
