from datetime import timedelta
import os
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pathlib import Path

from app_tools.core.config import Settings
from app_tools.models.user import User
from app_tools.core.security import security

settings = Settings()


conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
    MAIL_FROM=os.environ.get("MAIL_FROM"),
    MAIL_PORT=os.environ.get("MAIL_PORT", 587),
    MAIL_SERVER=os.environ.get("MAIL_SERVER"),
    MAIL_STARTTLS=os.environ.get("MAIL_STARTTLS"),
    MAIL_SSL_TLS=os.environ.get("MAIL_SSL_TLS"),
    USE_CREDENTIALS=os.environ.get("USE_CREDENTIALS"),
    VALIDATE_CERTS=True,
    MAIL_DEBUG=True,
    MAIL_FROM_NAME=settings.APP_NAME,
    # MAIL_FROM_NAME=os.environ.get("MAIL_FROM_NAME"),
    TEMPLATE_FOLDER=Path(__file__).parent.parent.parent/"templates",
)

fm = FastMail(conf)


def send_email(
    receiver: User,
    subject: str,
    context: dict,
    template_name: str,
    background_tasks: BackgroundTasks
) -> None:

    token_data = {"id": receiver.id, "email": receiver.email}
    token = security.generate_token(token_data, expires=timedelta(hours=24))
    context = {
        "name": receiver.email,
        "frontend_url": settings.FRONTEND_HOST,
        "verification_url": f"{settings.FRONTEND_HOST}/auth/verification/?token={token}",
        "app_name": settings.APP_NAME,
        "company_name": settings.COMPANY_NAME,
        "company_email": settings.COMPANY_EMAIL,
    }  # Add to template context

    message = MessageSchema(
        subject=subject,
        recipients=[receiver.email],  # recipient must be a list of str
        template_body=context,
        subtype=MessageType.html)

    background_tasks.add_task(
        fm.send_message, message=message, template_name=template_name
    )
