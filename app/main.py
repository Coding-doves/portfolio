from fastapi import FastAPI

from app_tools.routers.user_auth import user_route
from app_tools.routers.auth import email_router
from app_tools.routers.project import project_route
from app_tools.routers.skills import skills_route
from app_tools.routers.experience import experience_route
from app_tools.routers.education import education_route
from app_tools.routers.testimonials import testimonial_route
from app_tools.routers.contact import contact_route
from app_tools.routers.blog import blog_route
from app_tools.routers.blog_tag import tag_route

app = FastAPI()

app.include_router(router=user_route, prefix="/api/users", tags=["Users"],)
app.include_router(router=email_router, prefix="/api/auth", tags=["Email"],)
app.include_router(router=project_route, prefix="/api/project", tags=["Projects Management"],)
app.include_router(router=skills_route, prefix="/api/skills", tags=["Skills"],)
app.include_router(router=experience_route, prefix="/api/experience", tags=["Experience"],)
app.include_router(router=education_route, prefix="/api/education", tags=["Education"],)
app.include_router(router=testimonial_route, prefix="/api/testimonial", tags=["Testimonial"],)
app.include_router(router=contact_route, prefix="/api/contact", tags=["Contact"],)
app.include_router(router=blog_route, prefix="/api/blog", tags=["Blog"],)
app.include_router(router=tag_route, prefix="/api/tag", tags=["Tag"],)


@app.get("/")
def home():
    return {"key": "value"}
