from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
from app.db.connection import get_database
from app.models.models import Comment, User, UserLikeDislike
from fastapi import Depends

from app.schemas.comments import CommentCreate

class CommentRepository:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session

    async def create_comment(self, post_id: int, user_id: int, request: CommentCreate) -> Comment:
        new_comment = Comment(
            post_id=post_id,
            user_id=user_id,
            content=request.content,
            create_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        self.session.add(new_comment)
        await self.session.commit()
        await self.session.refresh(new_comment)
        return new_comment

    async def create_reply(self, post_id: int, user_id: int, parent_comment_id: int, content: str) -> Comment:
        new_reply = Comment(
            post_id=post_id,
            user_id=user_id,
            parent_id=parent_comment_id,
            content=content,
            create_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        self.session.add(new_reply)
        await self.session.commit()
        await self.session.refresh(new_reply)
        return new_reply
    
    async def delete_comment(self, comment_id: int):
        await self.session.execute(delete(Comment).where(Comment.id == comment_id))
        await self.session.commit()

    async def get_comment_by_id(self, comment_id: int) -> Comment | None:
        stmt = select(Comment).where(Comment.id == comment_id)
        result = await self.session.scalar(stmt)
        return result

    async def like_comment(self, user: User, comment: Comment):
        stmt = select(UserLikeDislike).where(
                UserLikeDislike.user_id == user.id, 
                UserLikeDislike.comment_id == comment.id
            )
        existing = await self.session.scalar(stmt)
        
        if existing:
            if existing.type == "like":
                await self.session.delete(existing)
                comment.likes -= 1
            elif existing.type == "dislike":
                existing.type = "like"
                comment.likes += 1
                comment.dislikes -= 1
        else:
            new_like = UserLikeDislike(user_id=user.id, comment_id=comment.id, type="like")
            self.session.add(new_like)
            comment.likes += 1
        
        await self.session.commit()
        
    async def dislike_comment(self, user: User, comment: Comment):
        stmt = select(UserLikeDislike).where(
                UserLikeDislike.user_id == user.id, 
                UserLikeDislike.comment_id == comment.id
            )
        existing = await self.session.scalar(stmt)
        
        if existing:
            if existing.type == "like":
                await self.session.delete(existing)
                comment.likes -= 1
            elif existing.type == "dislike":
                existing.type = "like"
                comment.likes += 1
                comment.dislikes -= 1
        else:
            new_like = UserLikeDislike(user_id=user.id, comment_id=comment.id, type="like")
            self.session.add(new_like)
            comment.likes += 1
        
        await self.session.commit()