from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from typing import List

from app_tools.core.db.database import get_session
from app_tools.dependencies.upload_img import upload_images
from app_tools.models.blog import BlogPost, BlogPostTag
from app_tools.schemas.blog import BlogPostCreate, BlogPostOut

blog_route = APIRouter()


# Create a new blog post
@blog_route.post("/", response_model=BlogPostOut, status_code=status.HTTP_201_CREATED)
def create_blog_post(blog: BlogPostCreate, db: Session = Depends(get_session)):
    # Create the blog post
    new_blog = BlogPost(
        title=blog.title,
        slug=blog.slug,
        content=blog.content,
        featured_image=blog.featured_image,
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    # Link tags using BlogPostTag
    for tag_id in blog.tag_ids:
        blog_tag = BlogPostTag(blog_post_id=new_blog.id, tag_id=tag_id)
        db.add(blog_tag)

    db.commit()
    db.refresh(new_blog)

    return new_blog


# Get a single blog post by ID
@blog_route.get("/{post_id}", response_model=BlogPostOut)
def get_blog_post(post_id: int, db: Session = Depends(get_session)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post


# Get all blog posts
@blog_route.get("/", response_model=List[BlogPostOut])
def list_blog_posts(db: Session = Depends(get_session)):
    return db.query(BlogPost).order_by(BlogPost.created_at.desc()).all()


# Update a blog post
@blog_route.put("/{post_id}", response_model=BlogPostOut)
def update_blog_post(post_id: int, blog: BlogPostCreate, db: Session = Depends(get_session)):
    existing = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    for key, value in blog.model_dump().items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing


# Delete a blog post
@blog_route.delete("/{post_id}", status_code=status.HTTP_200_OK)
def delete_blog_post(post_id: int, db: Session = Depends(get_session)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    db.delete(post)
    db.commit()
    return {"detail": f"Blog post (ID: {post_id}) deleted successfully"}


@blog_route.put("/upload-image/{blog_id}", status_code=status.HTTP_200_OK, response_model=BlogPostOut)
def upload_blog_images(blog_id: int, image: UploadFile = File(...), db: Session = Depends(get_session)):
    blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")

    # Save image to disk
    filepath = upload_images("blog", image)

    # Update the blog post
    blog.featured_image = filepath
    db.commit()
    db.refresh(blog)

    return blog
