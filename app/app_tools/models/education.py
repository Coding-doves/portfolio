from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from datetime import datetime
from app_tools.core.db.database import Base


class Education(Base):
    __tablename__ = "Education"

    id = Column(Integer, primary_key=True, index=True)
    degree = Column(String(150), nullable=False)
    institution = Column(String(150), nullable=False)
    location = Column(String(150))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
