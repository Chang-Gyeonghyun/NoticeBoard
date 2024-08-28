from typing import List
from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, model_validator

from app.schemas.comments import CommentInstance

class PostRequest(BaseModel):
    title: str
    content: str
    model_config = ConfigDict(from_attributes=True)
    
class PostUpdateRequest(PostRequest):
    pass
    
class PostFiles(BaseModel):
    id: int
    file_name: str
    model_config = ConfigDict(from_attributes=True)
    
class PostBase(BaseModel):
    id: int
    title: str
    userName: str
    create_datetime: str
    likes: int
    @model_validator(mode='before')
    def set_user_name(cls, values):
        values.userName = values.user.userName
        return values
    model_config = ConfigDict(from_attributes=True)

class PostInstance(PostBase):
    content: str
    dislikes: int
    last_update_datetime: str
    attachments: List[PostFiles] = []
    comments: List[CommentInstance] = []
    @model_validator(mode='before')
    def set_user_name(cls, values):
        values.userName = values.user.userName
        return values
    model_config = ConfigDict(from_attributes=True)
    
class PostsByPaging(BaseModel):
    currentPage: int
    items: List[PostBase]
    pageSize: int
    totalSize: int