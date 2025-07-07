from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app_tools.models.user import Profile


def get_profile_by_id(id: int, db: Session):
    profile = db.query(Profile).filter(Profile.id == id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user with that Id exists."
        )
    return profile

