import uuid

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from app_tools.core.db.database import Base


class User(Base):
    # A model representing a user in the database.
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(150))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(150))
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    verified_at = Column(
        DateTime, nullable=True, default=None, onupdate=datetime.now())
    updated_at = Column(
        DateTime, nullable=True, default=None, onupdate=datetime.now())
    created_at = Column(DateTime, nullable=False, server_default=func.now())
