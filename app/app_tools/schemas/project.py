from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# --- Project Category ---
class ProjectCategoryBase(BaseModel):
    name: str


class ProjectCategoryCreate(ProjectCategoryBase):
    pass


class ProjectCategoryOut(ProjectCategoryBase):
    id: int
    created_at: datetime

    class Config:
        ormfrom_attributes_mode = True


# --- Stack and Tool ---
class ProjectStackBase(BaseModel):
    stack_name: str


class ProjectToolBase(BaseModel):
    tool_name: str


class ProjectStackOut(ProjectStackBase):
    id: int

    class Config:
        from_attributes = True


class ProjectToolOut(ProjectToolBase):
    id: int

    class Config:
        from_attributes = True


# --- Project ---
class ProjectBase(BaseModel):
    title: str
    slug: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    github_link: Optional[str] = None
    live_demo_link: Optional[str] = None
    is_featured: Optional[bool] = False


class ProjectCreate(ProjectBase):
    categories: Optional[List[ProjectCategoryBase]] = []
    stacks: Optional[List[ProjectStackBase]] = []
    tools: Optional[List[ProjectToolBase]] = []


class ProjectUpdate(ProjectCreate):
    title: Optional[str] = None


class ProjectImageSchema(BaseModel):
    id: int
    image_url: Optional[str]
    image_upload: Optional[str]

    class Config:
        orm_mode = True

class ProjectVideoSchema(BaseModel):
    id: int
    video_url: Optional[str]
    video_upload: Optional[str]

    class Config:
        orm_mode = True


class ProjectOut(ProjectCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    images: List[ProjectImageSchema]
    videos: List[ProjectVideoSchema]

    

    class Config:
        from_attributes = True
