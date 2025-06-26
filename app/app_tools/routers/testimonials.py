from datetime import datetime
import os
import shutil
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from typing import List, Optional

from app_tools.dependencies.upload_img import upload_images
from app_tools.schemas.testimonial import TestimonialOut
from app_tools.core.db.database import get_session
from app_tools.models.testimonial import Testimonial

testimonial_route = APIRouter()


@testimonial_route.post('/', status_code=status.HTTP_201_CREATED, response_model=TestimonialOut)
def create_testimonial(
    name: str = Form(...),
    role: Optional[str] = Form(None),
    company: Optional[str] = Form(None),
    message: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_session)
):    
    # Handle image upload if provided
    if image:
        image_path = upload_images("testimonial", image)

    new_testim = Testimonial(
        name=name,
        role=role,
        company=company,
        message=message,
        image=image_path
    )

    db.add(new_testim)
    db.commit()
    db.refresh(new_testim)

    return new_testim
    

@testimonial_route.get('/', status_code=status.HTTP_200_OK, response_model=List[TestimonialOut])
def get_all_testimonials(db: Session = Depends(get_session)):
    return db.query(Testimonial).all()


@testimonial_route.get('/{testmonial_id}', status_code=status.HTTP_200_OK, response_model=TestimonialOut)
def get_testimonial(testimonial_id: int, db: Session = Depends(get_session)):
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
        
    return testimonial


@testimonial_route.put('/{testimonial_id}', status_code=status.HTTP_200_OK, response_model=TestimonialOut)
def edit_testimonial(
    testimonial_id: int,
    name: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    company: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
    db: Session = Depends(get_session)
):
    existing_testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()

    if not existing_testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    # Update text fields
    if existing_testimonial.name: existing_testimonial.name = name
    if existing_testimonial.role: existing_testimonial.role = role
    if existing_testimonial.company: existing_testimonial.company = company
    if existing_testimonial.message: existing_testimonial.message = message

    db.commit()
    db.refresh(existing_testimonial)

    return existing_testimonial


@testimonial_route.put('/{testimonial_id}/image', status_code=status.HTTP_200_OK, response_model=TestimonialOut)
def update_testimonial_image(
    testimonial_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_session)
):
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()

    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    # Delete old image file if it exists
    if testimonial.image and os.path.exists(testimonial.image):
        os.remove(testimonial.image)

    # Save new image
    if image:
        path = upload_images("testimonial", image)

    # Update testimonial record
    testimonial.image = path
    db.commit()
    db.refresh(testimonial)

    return testimonial


@testimonial_route.delete('/{testmonial_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_testimonial(testimonial_id: int, db: Session = Depends(get_session)):
    exsiting_testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    
    if not exsiting_testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    if exsiting_testimonial.image and os.path.exists(exsiting_testimonial.image):
        os.remove(exsiting_testimonial.image)
        
    db.delete(exsiting_testimonial)
    db.commit()
