from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app_tools.core.db.database import Base


class SkillCategory(Base):
    __tablename__ = "SkillCategory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True)

    skills = relationship("Skill", back_populates="category")


class Skill(Base):
    __tablename__ = "Skill"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    proficiency = Column(String(50))
    icon = Column(String(150))
    category_id = Column(Integer, ForeignKey("SkillCategory.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("SkillCategory", back_populates="skills")
