from fastapi import FastAPI

from app_tools.routers.user import user_route
from app_tools.routers.auth import email_router
from app_tools.routers.dashboard import dashboard_router
from app_tools.routers.owner.project import project

app = FastAPI()

app.include_router(router=user_route, prefix="/api/users", tags=["Users"],)
app.include_router(router=email_router, prefix="/api/auth", tags=["Email"],)
app.include_router(router=dashboard_router, prefix="/api/dashboard", tags=["Dashboard"],)
app.include_router(router=project, prefix="/api/project", tags=["Projects Management"],)


@app.get("/")
def home():
    return {"key": "value"}
