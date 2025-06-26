from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# --- Tag ---
class TagBase(BaseModel):
    name: str
    slug: Optional[str]


class TagCreate(TagBase):
    pass


class TagOut(TagBase):
    id: int

    class Config:
        from_attributes = True


# --- Blog Post Tag Link ---
class BlogPostTagOut(BaseModel):
    id: int
    tag: TagOut

    class Config:
        from_attributes = True


# --- Blog Post ---
class BlogPostBase(BaseModel):
    title: str
    slug: Optional[str]
    content: str
    featured_image: Optional[str]


class BlogPostCreate(BlogPostBase):
    tag_ids: Optional[List[int]] = []


class BlogPostOut(BlogPostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[BlogPostTagOut]

    class Config:
        from_attributes = True
