from fastapi import FastAPI

from app_tools.routers.user_auth import user_route
from app_tools.routers.auth import email_router
from app_tools.routers.dashboard import dashboard_router
from app_tools.routers.project import project_route
from app_tools.routers.skills import skills_route
from app_tools.routers.experience import experience_route
from app_tools.routers.education import education_route

app = FastAPI()

app.include_router(router=user_route, prefix="/api/users", tags=["Users"],)
app.include_router(router=email_router, prefix="/api/auth", tags=["Email"],)
app.include_router(router=dashboard_router, prefix="/api/dashboard", tags=["Dashboard"],)
app.include_router(router=project_route, prefix="/api/project", tags=["Projects Management"],)
app.include_router(router=skills_route, prefix="/api/skills", tags=["Skills"],)
app.include_router(router=experience_route, prefix="/api/experience", tags=["Experience"],)
app.include_router(router=education_route, prefix="/api/education", tags=["Education"],)


@app.get("/")
def home():
    return {"key": "value"}
