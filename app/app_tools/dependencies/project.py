from sqlalchemy.orm import Session
from typing import List

from app_tools.models import project


def get_project_by_id(project_id: int, db: Session) -> project.Project:
    return db.query(project.Project).filter(project.Project.id == project_id).first()


def extras(
    new_project: project.Project,
    db: Session,
    stacks: List[str] = [],
    tools: List[str] = [],
    categories: List[str] = [],
):
    # Add stack
    if len(stacks) > 0:
        for stk_name in stacks:
            stk = db.query(project.ProjectStack).filter_by(stack_name=stk_name).first()
            
            if not stk:
                stk = project.ProjectStack(stack_name=stk_name)
            new_project.stacks.append(stk)
    
    # Add tools
    if len(tools) > 0:    
        for tool_name in tools:
            tl = db.query(project.ProjectTool).filter_by(tool_name=tool_name).first()
            
            if not tl:
                tl = project.ProjectTool(tool_name=tool_name)
            new_project.tools.append(tl)
    
    # Add category
    if len(categories) > 0:
        for category_name in categories:
            category = db.query(project.ProjectCategory).filter_by(name=category_name).first()
            
            if not category:
                category = project.ProjectCategory(name=category_name)
            new_project.categories.append(category)

    return new_project
