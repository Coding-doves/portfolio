from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app_tools.core.db.database import get_session
from app_tools.dependencies.profile import get_profile_by_id
from app_tools.dependencies.upload_img import upload_images
from app_tools.dependencies.user import get_user_by_id
from app_tools.models.user import Profile
from app_tools.schemas.user import ProfileCreate, ProfileOut
from datetime import datetime
import shutil
import os

profile_route = APIRouter()


# Create or update profile
@profile_route.post("/", response_model=ProfileOut, status_code=status.HTTP_201_CREATED)
def create_or_update_profile(
    profile: ProfileCreate,
    user_id: str,
    db: Session = Depends(get_session)
):
    profile = get_user_by_id(user_id, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    existing_profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    if existing_profile:
        # Update existing profile
        for key, value in profile.model_dump(exclude_unset=True).items():
            setattr(existing_profile, key, value)
        existing_profile.updated_at = datetime.now()
        db.commit()
        db.refresh(existing_profile)
        return existing_profile

    # Create new profile
    new_profile = Profile(**profile.model_dump(), user_id=user_id)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


# Get a profile by user ID
@profile_route.get("/user/{user_id}", response_model=ProfileOut)
def get_profile(user_id: str, db: Session = Depends(get_session)):
    profile = get_profile_by_id(user_id, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


# Upload profile image
@profile_route.put("/{profile_id}/upload-image", response_model=ProfileOut)
def upload_profile_image(profile_id: int, image: UploadFile = File(...), db: Session = Depends(get_session)):
    profile = get_profile_by_id(profile_id, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    filename = upload_images("profile", image)

    if not filename:
        raise HTTPException(status_code=500, detail="Image upload failed")
    
    profile.profile_image = filename
    db.commit()
    db.refresh(profile)
    return profile
