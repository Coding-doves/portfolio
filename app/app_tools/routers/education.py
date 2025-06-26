from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app_tools.schemas.education import EducationCreate, EducationOut
from app_tools.core.db.database import get_session
from app_tools.models.education import Education


education_route = APIRouter()
