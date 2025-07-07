from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from app_tools.core.config import Settings
from app_tools.core.db.database import get_session
from app_tools.core.security.security import decode_token
from app_tools.dependencies.user import get_user_by_id
from app_tools.routers.profile import create_or_update_profile

email_router = APIRouter(responses={404: {"Description": "Page not found"}})
settings = Settings()
templates = Jinja2Templates(directory="templates")


@email_router.get("/verification", response_class=HTMLResponse)
def email_verification(
    request: Request, token: str, db: Session = Depends(get_session)
):
    try:
        user = decode_token(token, db)
    except HTTPException as e:
        return templates.TemplateResponse(
            "email_verification.html",
            {
                "request": request,
                "status": "error",
                "message": e.detail,
            },
        )

    user_data = get_user_by_id(user['id'], db)

    # Prevent re-verification
    if user_data.is_verified:
        return templates.TemplateResponse(
            "email_verification.html",
            {
                "request": request,
                "status": "already_verified",
                "name": user_data.email,
            },
        )

    # Update the user's verification status
    user_data.is_verified = True
    user_data.is_active = True
    user_data.updated_at = datetime.utcnow()
    user_data.verified_at = datetime.utcnow()
    # Save the changes to the database
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    
    # Create profile for user
    profile_create = {
        "username": user_data.email.split("@")[0],
    }
    create_or_update_profile(profile=profile_create, user_id=user_data.id, db=db)

    return templates.TemplateResponse(
        "email_verification.html",
        {
            "request": request,
            "status": "success",
            "name": user_data.email,
        }
    )


@email_router.get("/verification_API", response_class=JSONResponse)
def email_verification_api(token: str, db: Session = Depends(get_session)):
    try:
        user = verify_token(token=token, token_type="verify", db=db)
    except HTTPException as e:
        raise HTTPException(status_code=401, detail=e.detail)

    if user.is_verified:
        return {
                "status": "already_verified",
                "name": user.name,
                }

    # Update the user's verification status
    user.is_verified = True
    user.is_active = True
    user.updated_at = datetime.utcnow()
    user.verified_at = datetime.utcnow()
    # Save the changes to the database
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
            "status": "success",
            "name": user.name,
            }
