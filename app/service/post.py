import os
import secrets

from fastapi import Depends, UploadFile
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from app.models.models import Post, User

class PostService:
    
    def create_search_query(
            self, entire: str | None = None, 
            userName: str | None = None, 
            title: str | None = None
        ):
        query = select(Post)
        
        if entire:
            query = query.where(
                or_(
                    Post.title.ilike(f"%{entire}%"),
                    Post.content.ilike(f"%{entire}%"),
                    Post.user.has(User.userName.ilike(f"%{entire}%"))
                )
            )
        
        if userName:
            query = query.where(Post.user.has(User.userName.ilike(f"%{userName}%")))
        
        if title:
            query = query.where(Post.title.ilike(f"%{title}%"))
        
        query = query.options(selectinload(Post.user))
        
        return query
    
    async def build_comment_tree(self, comments):
        comment_dict = {comment.id: comment for comment in comments}
        root_comments = []

        for comment in comments:
            if comment.parent_id:
                parent = comment_dict.get(comment.parent_id)
                if parent:
                    if not hasattr(parent, 'replies'):
                        parent.replies = []
            else:
                root_comments.append(comment)

        return root_comments