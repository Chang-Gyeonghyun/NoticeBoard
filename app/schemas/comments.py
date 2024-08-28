from typing import List, Optional
from pydantic import BaseModel, ConfigDict, model_validator

class CommentCreate(BaseModel):
    content: str
        
class CommentInstance(BaseModel):
    id: int
    content: str
    create_datetime: str
    userName: str
    likes: int
    dislikes: int
    parent_id: int | None
    replies: Optional[List['CommentInstance']] = []

    @model_validator(mode='before')
    def set_user_name(cls, values):
        user = values.user
        if user:
            values.userName = user.userName
        return values

    model_config = ConfigDict(from_attributes=True)