from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app_tools.core.db.database import get_session
from app_tools.models.blog import Tag
from app_tools.schemas.blog import TagCreate, TagOut

tag_route = APIRouter()

@tag_route.post("/", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagCreate, db: Session = Depends(get_session)):
    existing = db.query(Tag).filter((Tag.name == tag.name) | (Tag.slug == tag.slug)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag with this name or slug already exists")

    new_tag = Tag(**tag.model_dump())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@tag_route.get("/", response_model=List[TagOut])
def get_all_tags(db: Session = Depends(get_session)):
    return db.query(Tag).all()

@tag_route.get("/{tag_id}", response_model=TagOut)
def get_tag(tag_id: int, db: Session = Depends(get_session)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@tag_route.put("/{tag_id}", response_model=TagOut)
def update_tag(tag_id: int, updated: TagCreate, db: Session = Depends(get_session)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    for key, val in updated.model_dump().items():
        setattr(tag, key, val)

    db.commit()
    db.refresh(tag)
    return tag

@tag_route.delete("/{tag_id}", status_code=status.HTTP_200_OK)
def delete_tag(tag_id: int, db: Session = Depends(get_session)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()
    return {"detail": "Tag deleted successfully"}
