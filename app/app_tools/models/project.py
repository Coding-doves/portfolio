from sqlalchemy import Column, Integer, String, Table, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app_tools.core.db.database import Base


project_category = Table(
    'project_category',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('Project.id', ondelete="CASCADE"), primary_key=True),
    Column('category_id', Integer, ForeignKey('ProjectCategory.id', ondelete="CASCADE"), primary_key=True)
)

project_stack = Table(
    'project_stack',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('Project.id', ondelete="CASCADE"), primary_key=True),
    Column('stack_id', Integer, ForeignKey('ProjectStack.id', ondelete="CASCADE"), primary_key=True)
)

project_tool = Table(
    'project_tool',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('Project.id', ondelete="CASCADE"), primary_key=True),
    Column('tool_id', Integer, ForeignKey('ProjectTool.id', ondelete="CASCADE"), primary_key=True)
)


class Project(Base):
    __tablename__ = "Project"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    slug = Column(String(150), unique=True)
    summary = Column(Text)
    description = Column(Text)
    github_link = Column(String(255))
    live_demo_link = Column(String(255))
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    categories = relationship("ProjectCategory", secondary=project_category, back_populates="projects")
    stacks = relationship("ProjectStack", secondary=project_stack, back_populates="project", cascade="all, delete")
    tools = relationship("ProjectTool", secondary=project_tool, back_populates="project", cascade="all, delete")
    images = relationship("ProjectImage", cascade="all, delete", back_populates="project")
    videos = relationship("ProjectVideo", cascade="all, delete", back_populates="project")


# models/project.py
class ProjectImage(Base):
    __tablename__ = "project_images"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("Project.id", ondelete="CASCADE"))
    
    image_url = Column(String(255), nullable=True)      # For external image links (e.g., imgur, Cloudinary)
    image_upload = Column(String(255), nullable=True)   # For device-uploaded file paths (e.g., media/images/filename.jpg)

    project = relationship("Project", back_populates="images")


class ProjectVideo(Base):
    __tablename__ = "project_videos"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("Project.id", ondelete="CASCADE"))
    
    video_url = Column(String(255), nullable=True)      # For YouTube/Vimeo/Cloudflare etc.
    video_upload = Column(String(255), nullable=True)   # Local path to uploaded video

    project = relationship("Project", back_populates="videos")


class ProjectCategory(Base):
    __tablename__ = "ProjectCategory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    projects = relationship("Project", secondary=project_category, back_populates="categories")


class ProjectStack(Base):
    __tablename__ = "ProjectStack"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("Project.id", ondelete="CASCADE"))
    stack_name = Column(String(100), nullable=False)

    project = relationship("Project", back_populates="stacks")


class ProjectTool(Base):
    __tablename__ = "ProjectTool"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("Project.id", ondelete="CASCADE"))
    tool_name = Column(String(100), nullable=False)

    project = relationship("Project", back_populates="tools")
