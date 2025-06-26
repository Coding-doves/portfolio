from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app_tools.core.db.database import Base


class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Client's name
    role = Column(String(100), nullable=True)    # e.g., CEO, Manager
    company = Column(String(100), nullable=True) # Optional company name
    message = Column(Text, nullable=False)       # The testimonial content
    image = Column(String(255), nullable=True)   # Optional image path or URL
    created_at = Column(DateTime(timezone=True), server_default=func.now())
