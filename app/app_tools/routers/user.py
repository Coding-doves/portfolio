from datetime import datetime
from fastapi import APIRouter, status, Depends, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app_tools.core.db import redis
from app_tools.core.db.database import get_session
from app_tools.core.security import auth_bearer
from app_tools.core.security import security
from app_tools.schemas.user import LoginResponse, UserCreate
from app_tools.schemas.message import UserWithMessageResponse
from app_tools.dependencies import user

user_route = APIRouter(responses={404: {"Description": "Page not found"}})


@user_route.post(
    "/sign_up",
    response_model=UserWithMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def new_user(
    data: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_session)
) -> UserWithMessageResponse:
    new_user = user.register_user(data, db, background_tasks)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User registration failed"
        )

    return {
        "user": new_user,
        "message": {
            "detail": "Verification email sent. Please check your mail inbox"
        }
    }


@user_route.post(
    "/signin", status_code=status.HTTP_200_OK, response_model=LoginResponse,
)
def signin(
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
) -> LoginResponse:
    """Sign in a user and return access and refresh tokens"""
    return user.get_access_token(data=data, db=db)


@user_route.get('/refresh_token')
def get_new_access_token(
    token_details: dict = Depends(auth_bearer.RefreshTokenBearer())
):
    print(f'From refresh_token api: {token_details}')
    timestamp_expiry = token_details['exp']
    refresh_token = security.generate_token(
        data={"id": token_details['id'], "email": token_details['email'], "refresh": True},
        token_type="refresh",
    )
        
    return JSONResponse(content={'access_token': refresh_token})


@user_route.post('/logout')
def revoke_token(
    token_details: dict = Depends(auth_bearer.RefreshTokenBearer())
):
    """
    Logout the user by blacklisting the refresh token.
    """
    if not token_details:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired token"
        )
    print(token_details)
    # Blacklist the refresh token
    redis.add_token_to_blacklist(token=token_details['refresh'])

    return JSONResponse(
        content={"message": "User logged out successfully"},
        status_code=status.HTTP_200_OK
    )
