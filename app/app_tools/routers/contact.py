from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app_tools.core.db.database import get_session
from app_tools.models.contact import ContactMessage
from app_tools.schemas.contact import ContactMessageCreate, ContactMessageOut


contact_route = APIRouter()


@contact_route.post('/', status_code=status.HTTP_201_CREATED, response_model=ContactMessageOut)
def create_contact_message(data: ContactMessageCreate, db: Session = Depends(get_session)):
    contact = ContactMessage(**data.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    
    return contact


@contact_route.get('/', status_code=status.HTTP_200_OK, response_model=List[ContactMessageOut])
def get_all_msg(db: Session = Depends(get_session)):
    return db.query(ContactMessage).all()


@contact_route.get('/{msg_id}', status_code=status.HTTP_200_OK, response_model=ContactMessageOut)
def get_msg(msg_id: int, db: Session = Depends(get_session)):
    message = db.query(ContactMessage).filter(ContactMessage.id == msg_id).first()
    
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        
    return message

@contact_route.delete('/{msg_id}', status_code=status.HTTP_204_NO_CONTENT)
def del_msg(msg_id: int, db: Session = Depends(get_session)):
    message = db.query(ContactMessage).filter(ContactMessage.id == msg_id).first()
    
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    
    db.delete(message)
    db.commit()
