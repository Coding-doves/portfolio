from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app_tools.schemas.skills import SkillCategoryCreate, SkillCategoryOut, SkillOut, SkillCreate
from app_tools.core.db.database import get_session
from app_tools.models.skills import Skill, SkillCategory

skills_route = APIRouter()


@skills_route.get("/", status_code=status.HTTP_200_OK, response_model=List[SkillOut]) 
def get_skills(db: Session = Depends(get_session)):
    """
    Retrieve all skills.
    """
    return db.query(Skill).all()


@skills_route.get("/category", response_model=List[SkillCategoryOut])
def get_all_categories(db: Session = Depends(get_session)):
    """
    Retrieve all SkillCategory.
    """
    return db.query(SkillCategory).all()


@skills_route.get("/{skill_id}", status_code=status.HTTP_200_OK, response_model=SkillOut)
def get_skill(skill_id: int, db: Session = Depends(get_session)):
    """
    Retrieve a skill by its ID.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@skills_route.get("/category/{category_id}", response_model=SkillCategoryOut)
def get_single_category(category_id: int, db: Session = Depends(get_session)):
    """
    Retrieve all SkillCategory.
    """
    skill_cat = db.query(SkillCategory).filter(SkillCategory.id == category_id).first()
    if not skill_cat:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill_cat


@skills_route.post("/category", status_code=status.HTTP_201_CREATED, response_model=SkillCategoryOut)
def create_skill_category(category: SkillCategoryCreate, db: Session = Depends(get_session)):
    new_category = SkillCategory(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@skills_route.post("/", status_code=status.HTTP_201_CREATED, response_model=SkillOut)
def create_skill(skill: SkillCreate, db: Session = Depends(get_session)):
    category = None
    if skill.category_id:
        category = db.query(SkillCategory).filter(SkillCategory.id == skill.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    new_skill = Skill(**skill.model_dump())
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill


@skills_route.put("/{skill_id}", status_code=status.HTTP_200_OK, response_model=SkillOut)
def update_skill(skill_id: int, skill: SkillCreate, db: Session = Depends(get_session)):
    """
    Update an existing skill.
    """
    existing_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not existing_skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # Optional: Validate category_id if provided
    if skill.category_id:
        category = db.query(SkillCategory).filter(SkillCategory.id == skill.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    for key, value in skill.dict(exclude_unset=True).items():
        setattr(existing_skill, key, value)

    db.commit()
    db.refresh(existing_skill)
    return existing_skill


@skills_route.put("/category/{category_id}", status_code=status.HTTP_200_OK, response_model=SkillCategoryOut)
def update_skill_category(category_id: int, category: SkillCategoryCreate, db: Session = Depends(get_session)):
    """
    Update an existing skill category.
    """
    existing_category = db.query(SkillCategory).filter(SkillCategory.id == category_id).first()
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(existing_category, key, value)

    db.commit()
    db.refresh(existing_category)
    return existing_category


@skills_route.delete("/skill/{skill_id}", status_code=status.HTTP_200_OK)
def delete_skill(skill_id: int, db: Session = Depends(get_session)) -> dict:
    """
    Delete a skill by its ID.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(skill)
    db.commit()
    return {"detail": "Skill deleted successfully"}


@skills_route.delete("/category/{category_id}", status_code=status.HTTP_200_OK)
def delete_skill_category(category_id: int, db: Session = Depends(get_session)) -> dict:
    """
    Delete a skill category by its ID.
    """
    category = db.query(SkillCategory).filter(SkillCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"detail": "Category deleted successfully"}

