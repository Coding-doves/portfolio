from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app_tools.schemas.education import EducationCreate, EducationOut
from app_tools.core.db.database import get_session
from app_tools.models.education import Education


education_route = APIRouter()


@education_route.post("/", response_model=EducationOut, status_code=status.HTTP_201_CREATED)
def create_education(
    education: EducationCreate,
    db: Session = Depends(get_session)
):
    new_education = Education(**education.model_dump())
    db.add(new_education)
    db.commit()
    db.refresh(new_education)
    return new_education


@education_route.get("/", response_model=List[EducationOut])
def get_educations(db: Session = Depends(get_session)):
    return db.query(Education).all()


@education_route.get("/{education_id}", response_model=EducationOut)
def get_education(
    education_id: int,
    db: Session = Depends(get_session)
):
    education = db.query(Education).filter(Education.id == education_id).first()
    if not education:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")
    return education


@education_route.put("/{education_id}", response_model=EducationOut)
def update_education(
    education_id: int,
    education: EducationCreate,
    db: Session = Depends(get_session)
):
    existing_education = db.query(Education).filter(Education.id == education_id).first()
    if not existing_education:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")
    
    for key, value in education.model_dump().items():
        setattr(existing_education, key, value)
    
    db.commit()
    db.refresh(existing_education)
    return existing_education


@education_route.delete("/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education(
    education_id: int,
    db: Session = Depends(get_session)
):
    education = db.query(Education).filter(Education.id == education_id).first()
    if not education:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")
    
    db.delete(education)
    db.commit()
    return None
