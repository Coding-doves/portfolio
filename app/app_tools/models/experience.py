from app_tools.models.enums import LearningModeEnum

from sqlalchemy import Column, Enum, Integer, String, Text, Date, DateTime
from datetime import datetime
from app_tools.core.db.database import Base


class Experience(Base):
    __tablename__ = "Experience"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(150), nullable=False)
    company = Column(String(150), nullable=False)
    location = Column(String(150))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    description = Column(Text)
    job_mode = Column(Enum(LearningModeEnum), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
