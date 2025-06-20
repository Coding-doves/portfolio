from pydantic import BaseModel

from app_tools.schemas.user import UserResponse


class MessageResponse(BaseModel):
    detail: str


class UserWithMessageResponse(BaseModel):
    user: UserResponse
    message: MessageResponse
