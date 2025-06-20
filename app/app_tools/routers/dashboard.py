from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app_tools.core.security import auth_bearer
from app_tools.core.db.database import get_session

access_token_bearer = auth_bearer.AccessTokenBearer()
dashboard_router = APIRouter()


@dashboard_router.get("/")
def dashboard(
    db: Session = Depends(get_session), user_auth: str = Depends(access_token_bearer)
):
    return {
        "message": "Welcome to the dashboard",
        "user": user_auth
    }
