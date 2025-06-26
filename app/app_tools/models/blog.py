from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app_tools.core.db.database import Base


class BlogPost(Base):
    __tablename__ = "BlogPost"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True)
    content = Column(Text, nullable=False)
    featured_image = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.utcnow)

    tags = relationship("BlogPostTag", back_populates="blog_post", cascade="all, delete")


class Tag(Base):
    __tablename__ = "Tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True)

    blog_tags = relationship("BlogPostTag", back_populates="tag", cascade="all, delete")


class BlogPostTag(Base):
    __tablename__ = "BlogPostTag"

    id = Column(Integer, primary_key=True, index=True)
    blog_post_id = Column(Integer, ForeignKey("BlogPost.id", ondelete="CASCADE"))
    tag_id = Column(Integer, ForeignKey("Tag.id", ondelete="CASCADE"))

    blog_post = relationship("BlogPost", back_populates="tags")
    tag = relationship("Tag", back_populates="blog_tags")
