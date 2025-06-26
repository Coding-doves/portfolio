import enum
import uuid

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, func, ForeignKey, Text
from sqlalchemy.orm import relationship

from app_tools.core.db.database import Base


class UserRole(str, enum.Enum):
    root = "root"
    admin = "admin"


class User(Base):
    # A model representing a user in the database.
    __tablename__ = 'User'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(150))
    role = Column(Enum(UserRole), default=UserRole.admin, nullable=False)
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    verified_at = Column(
        DateTime, nullable=True, default=None, onupdate=datetime.now())
    updated_at = Column(
        DateTime, nullable=True, default=None, onupdate=datetime.now())
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    profile = relationship("Profile", back_populates="user", uselist=False)


class Profile(Base):
    __tablename__ = "Profile"

    id = Column(Integer, primary_key=True, autoincrement=True,index=True)
    user_id = Column(String(36), ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    username = Column(String(100), unique=True)
    bio = Column(Text())
    location = Column(String(150))
    profile_image = Column(String(255))
    resume_link = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")
