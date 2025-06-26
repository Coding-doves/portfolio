from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm

from app_tools.core.email import send_email
from app_tools.core.security import security
from app_tools.models.user import User
from app_tools.schemas.user import UserCreate, LoginResponse


def register_user(
    data: UserCreate, session: Session, background_tasks: BackgroundTasks
) -> User:
    if not security.password_meets_criteria(data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 7 characters long, "
                   "contain at least one digit, one lowercase letter, "
                   "and one uppercase letter."
        )

    user_exist = get_user_by_email(data.email, session)
    
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email exists in database."
        )

    user = User(
        name=data.name,
        email=data.email,
        password=security.hash_password(data.password),
        updated_at=datetime.utcnow()
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Account verification via email
    send_email(
        receiver=user,
        subject="Confirm your registration",
        context={},
        template_name="verify_email.html",
        background_tasks=background_tasks
    )

    return user


def get_access_token(
    data: OAuth2PasswordRequestForm,
    db: Session,
) -> LoginResponse:
    # Verify user login details is correct.
    # OAuth2PasswordRequestForm has only username and password.
    # So the username section is user of retrieve email
    user = get_user_by_email(data.username, db)
    if not user or \
            not security.verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password."
        )

    # Verify if user is verified
    if not user.is_verified:
        # Calculate how long since the user was created
        time_since_creation = datetime.utcnow() - user.created_at
        # If the user was created more than a day ago, send verification email again
        if time_since_creation > timedelta(hours=24):
            # Send verification email again
            send_email(
                receiver=user,
                subject="Resend Verification Email",
                context={},
                template_name="verify_email.html"
            )
        # Raise an exception to inform the user
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are unverified."
                   "Please check your email for the verificaion link"
        )

    # Verify if user is deactivated
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You account has been deactivated."
                   "Please contact support: contact@gmail.com"
        )

    # Generate access token and refresh token
    access_token = security.generate_token(
        data={"id": user.id, "email": user.email},
        token_type="access",
    )

    refresh_token = security.generate_token(
        data={"id": user.id, "email": user.email, "refresh": True},
        token_type="refresh",
        expires=timedelta(days=4)  # Refresh token valid for 30 days
    )

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=datetime.utcnow() + timedelta(hours=1),
        user={"user_id": user.id, "email": user.email},
    )


def get_user_by_email(data: str, db: Session):
    user = db.query(User).filter(User.email == data).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user with that email exists."
        )
    return user


def get_user_by_id(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user with that Id exists."
        )
    return user
