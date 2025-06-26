from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app_tools.schemas.experience import ExperienceCreate, ExperienceOut
from app_tools.core.db.database import get_session
from app_tools.models.experience import Experience

experience_route = APIRouter()


@experience_route.post("/", response_model=ExperienceOut, status_code=status.HTTP_201_CREATED)
def create_experience(
    experience: ExperienceCreate,
    db: Session = Depends(get_session)
):
    new_experience = Experience(**experience.model_dump())
    db.add(new_experience)
    db.commit()
    db.refresh(new_experience)
    return new_experience


@experience_route.get("/", response_model=List[ExperienceOut])
def get_experiences(
    db: Session = Depends(get_session)
):
    experiences = db.query(Experience).all()
    return experiences


@experience_route.get("/{experience_id}", response_model=ExperienceOut)
def get_experience(
    experience_id: int,
    db: Session = Depends(get_session)
):
    experience = db.query(Experience).filter(Experience.id == experience_id).first()
    if not experience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
    return experience


@experience_route.put("/{experience_id}", response_model=ExperienceOut)
def update_experience(
    experience_id: int,
    experience: ExperienceCreate,
    db: Session = Depends(get_session)
):
    existing_experience = db.query(Experience).filter(Experience.id == experience_id).first()
    if not existing_experience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
    
    for key, value in experience.model_dump().items():
        setattr(existing_experience, key, value)
    
    db.commit()
    db.refresh(existing_experience)
    return existing_experience


@experience_route.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experience(
    experience_id: int,
    db: Session = Depends(get_session)
):
    experience = db.query(Experience).filter(Experience.id == experience_id).first()
    if not experience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
    
    db.delete(experience)
    db.commit()
    return
