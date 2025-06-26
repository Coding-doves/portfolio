import re
from sqlalchemy.orm import Session
from app_tools.models import project


def slugify(text: str) -> str:
    # Remove unwanted characters
    text = re.sub(r"[^\w\s]", "", text).strip().lower()
    # Replace spaces/hyphens with a single hyphen, and return the slug
    return re.sub(r"[-\s]+", "-", text)


def generate_slug(title: str, db: Session, model, slug_field="slug") -> str:
    slugged =  slugify(title)
    slug = slugged
    num = 1
    
    while db.query(model).filter(getattr(model, slug_field) == slugged).first():
        slug = f"{slugged}-{num}"
        num += 1
        
    return slug
    