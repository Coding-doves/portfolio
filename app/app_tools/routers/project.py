from datetime import datetime
import os
import shutil

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app_tools.core.db.database import get_session
from app_tools.dependencies.slug import generate_slug
from app_tools.models import project
from app_tools.dependencies.project import extras, get_project_by_id
from app_tools.schemas.project import ProjectOut

project_route = APIRouter(responses={404: {"Description": "Page not found"}})   


@project_route.get("/", status_code=status.HTTP_200_OK, response_model=List[ProjectOut]) 
def get_all_projects(db: Session = Depends(get_session)):
    """
    Retrieve a list of projects.
    """
    projects = db.query(project.Project).all()
    return projects


@project_route.get("/{project_id}", status_code=status.HTTP_200_OK, response_model=ProjectOut) 
def get_project(project_id: int, db: Session = Depends(get_session)):
    projt = get_project_by_id(project_id, db)
        
    if not projt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return projt


@project_route.get("/slug/{slug}", response_model=ProjectOut)
def get_project_by_slug(slug: str, db: Session = Depends(get_session)):
    projt = db.query(project.Project).filter(project.Project.slug == slug).first()
    if not projt:
        raise HTTPException(status_code=404, detail="Project not found")
    return projt


@project_route.post("/", status_code=status.HTTP_200_OK, response_model=ProjectOut)
def add_project(
    title: str = Form(...),
    slug: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    github_link: Optional[str] = Form(None),
    live_demo_link: Optional[str] = Form(None),
    is_featured: Optional[bool] = Form(False),
    stacks: List[str] = Form([]),
    tools: List[str] = Form([]),
    categories: List[str] = Form([]),
    db: Session = Depends(get_session)
):
      
    if not slug:
        slug = generate_slug(title, db, project.Project)
            
    new_project = project.Project(
        title=title,
        slug=slug,
        summary=summary,
        description=description,
        github_link=github_link,
        live_demo_link=live_demo_link,
        is_featured=is_featured
    )
    
    # Add stacks, tools and category
    new_project = extras(new_project, db, stacks, tools, categories)
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project
    

@project_route.put("/{pro_id}", status_code=status.HTTP_200_OK)
def edit_project(
    pro_id: int,
    title: Optional[str] = Form(None),
    slug: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    github_link: Optional[str] = Form(None),
    live_demo_link: Optional[str] = Form(None),
    is_featured: Optional[bool] = Form(False),
    stacks: List[str] = Form([]),
    tools: List[str] = Form([]),
    categories: List[str] = Form([]),
    db: Session = Depends(get_session)
) -> ProjectOut:
    projt = get_project_by_id(pro_id, db)
    if not projt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
        
    # Updating
    if title and title != projt.title:
        projt.title = title
        if not slug:
            # Generate a new slug if title is provided and slug is not
            projt.slug = generate_slug(title, db, project.Project)
        else:
            projt.slug = slug

    if summary: projt.summary = summary
    if description: projt.description = description
    if github_link: projt.github_link = github_link
    if live_demo_link: projt.live_demo_link = live_demo_link
    if is_featured : projt.is_featured = is_featured
        
    # Update stacks, tools and category
    if stacks:
        projt.stacks.clear()
        projt = extras(projt, db, stacks)
    if tools:
        projt.tools.clear()
        projt = extras(projt, db, tools=tools)
    if categories:
        projt.categories.clear()
        projt = extras(projt, db, categories=categories)
    
    db.commit()
    db.refresh(projt)
    
    return projt  


@project_route.put("/img/{project_id}", status_code=status.HTTP_200_OK, response_model=ProjectOut)
def add_image_via_upload(
    project_id: int,
    image_uploads: List[UploadFile] = File(...),
    db: Session = Depends(get_session)
):
    projt = get_project_by_id(project_id, db)
    if not projt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Handle each image upload
    for img in image_uploads:
        filename = f"{datetime.now().timestamp()}_{img.filename}"
        path = f"media/images/{filename}"
        
        # Save file to disk
        with open(path, "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

        # Save image path to DB
        project_image = project.ProjectImage(project_id=projt.id, image_upload=path)
        db.add(project_image)

    db.commit()
    db.refresh(projt)
    
    return projt


@project_route.put("/video/{project_id}", status_code=status.HTTP_200_OK, response_model=ProjectOut)
def add_video_via_upload(
    project_id: int,
    video_uploads: List[UploadFile] = File(...),
    db: Session = Depends(get_session)
):
    projt = get_project_by_id(project_id, db)
    if not projt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    for video in video_uploads:
        filename = f"{datetime.utcnow().timestamp()}_{video.filename}"
        path = f"media/videos/{filename}"

        # Save file to disk
        with open(path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        # Save video path to DB
        project_video = project.ProjectVideo(project_id=projt.id, video_upload=path)
        db.add(project_video)

    db.commit()
    db.refresh(projt)

    return projt


@project_route.put("/video_image_link/{project_id}", status_code=status.HTTP_200_OK, response_model=ProjectOut)
def media_from_url(
    project_id: int,
    image_links: List[str] = Form([]),
    video_links: List[str] = Form([]),
    db: Session = Depends(get_session)
):
    projt = get_project_by_id(project_id, db)
    if not projt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Save new image links
    for img_url in image_links:
        db.add(project.ProjectImage(project_id=projt.id, image_link=img_url))

    # Save new video links
    for vid_url in video_links:
        db.add(project.ProjectVideo(project_id=projt.id, video_link=vid_url))

    db.commit()
    db.refresh(projt)

    return projt


@project_route.delete("/delete/{project_id}", status_code=status.HTTP_200_OK)
def delete_project(project_id: int, db: Session = Depends(get_session)):
    project = get_project_by_id(project_id, db)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Delete associated image files
    for img in project.images:
        if img.image_upload and os.path.exists(img.image_upload):
            os.remove(img.image_upload)
        db.delete(img)

    # Delete associated video files
    for vid in project.videos:
        if vid.video_upload and os.path.exists(vid.video_upload):
            os.remove(vid.video_upload)
        db.delete(vid)

    # Delete the project itself
    db.delete(project)
    db.commit()

    return {"message": f"Project (ID: {project_id}) deleted successfully"}


@project_route.delete("/delete_img/{project_id}", status_code=status.HTTP_200_OK)
def delete_project_images(project_id: int, db: Session = Depends(get_session)):
    projt = get_project_by_id(project_id, db)

    if not projt:
        raise HTTPException(status_code=404, detail="Project not found")

    # Delete each uploaded image file
    for img in projt.images:
        if img.image_upload and os.path.exists(img.image_upload):
            os.remove(img.image_upload)
        db.delete(img)

    db.commit()
    return {"message": f"All images for Project ID {project_id} have been deleted."}


@project_route.delete("/delete_img/{project_id}/{image_id}", status_code=status.HTTP_200_OK)
def delete_single_project_image(project_id: int, image_id: int, db: Session = Depends(get_session)):
    # Check if project exists
    projt = get_project_by_id(project_id, db)
    if not projt:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if the image belongs to the project
    img = db.query(project.ProjectImage).filter(
        project.ProjectImage.id == image_id,
        project.ProjectImage.project_id == project_id
    ).first()

    if not img:
        raise HTTPException(status_code=404, detail="Image not found for this project")

    # Delete image file from storage
    if img.image_upload and os.path.exists(img.image_upload):
        os.remove(img.image_upload)

    # Remove image record from DB
    db.delete(img)
    db.commit()

    return {"message": f"Image ID {image_id} deleted from project {project_id}"}


@project_route.delete("/delete_all_videos/{project_id}", status_code=status.HTTP_200_OK)
def delete_all_project_videos(project_id: int, db: Session = Depends(get_session)):
    projt = get_project_by_id(project_id, db)
    if not projt:
        raise HTTPException(status_code=404, detail="Project not found")

    videos = db.query(project.ProjectVideo).filter(project.ProjectVideo.project_id == project_id).all()

    for vid in videos:
        if vid.video_upload and os.path.exists(vid.video_upload):
            os.remove(vid.video_upload)
        db.delete(vid)

    db.commit()
    return {"message": f"All videos deleted from project {project_id}"}


@project_route.delete("/delete_video/{project_id}/{video_id}", status_code=status.HTTP_200_OK)
def delete_single_project_video(project_id: int, video_id: int, db: Session = Depends(get_session)):
    projt = get_project_by_id(project_id, db)
    if not projt:
        raise HTTPException(status_code=404, detail="Project not found")

    vid = db.query(project.ProjectVideo).filter(
        project.ProjectVideo.id == video_id,
        project.ProjectVideo.project_id == project_id
    ).first()

    if not vid:
        raise HTTPException(status_code=404, detail="Video not found for this project")

    if vid.video_upload and os.path.exists(vid.video_upload):
        os.remove(vid.video_upload)

    db.delete(vid)
    db.commit()

    return {"message": f"Video ID {video_id} deleted from project {project_id}"}
