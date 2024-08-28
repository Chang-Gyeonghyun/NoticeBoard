from datetime import datetime
from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.connection import get_database
from app.schemas import posts
from app.models.models import Comment, Post, User, UserLikeDislike
from app.service.post import PostService
from app.utils.paging import paginated_query

class PostRepository:
    def __init__(self, session: AsyncSession = Depends(get_database), service: PostService = Depends()):
        self.session = session
        self.service = service
               

    async def create_post(self, post_form: posts.PostRequest, user: User) -> Post:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')  
        
        new_post = Post(
            title=post_form.title,
            content=post_form.content,
            create_datetime=current_time,  
            last_update_datetime=current_time,
            user_id=user.id
        )
        
        self.session.add(new_post)
        await self.session.commit()
        await self.session.refresh(new_post)
        return new_post    
    
    async def get_posts_by_page(self, query, pageNo: int, pageSize: int):
        items, total_page = await paginated_query(query, pageNo, pageSize, self.session)
        return items, total_page
        
    async def get_post_by_id(self, post_id: int) -> Post:
        item = await self.session.scalar(
            select(Post)
            .where(Post.id == post_id)
            .options(
                selectinload(Post.user),
                selectinload(Post.comments).selectinload(Comment.user),
                selectinload(Post.comments).selectinload(Comment.replies).selectinload(Comment.user),
                selectinload(Post.attachments)
            )
        )
        return item
    
    async def delete_post(self, post_id: int) -> Post:
        await self.session.execute(delete(Post).where(Post.id == post_id))
        await self.session.commit()

    async def update_post(self, post_id: int, post_data: posts.PostUpdateRequest):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')  
        stmt = (
            update(Post)
            .where(Post.id == post_id)
            .values(
                title=post_data.title, 
                contents=post_data.contents, 
                last_update_datetime=current_time
                )
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(stmt)
        await self.session.commit()
        
    async def like_post(self, user: User, post: Post):
        stmt = select(UserLikeDislike).where(
                UserLikeDislike.user_id == user.id, 
                UserLikeDislike.post_id == post.id
            )
        existing = await self.session.scalar(stmt)
        
        if existing:
            if existing.type == "like":
                await self.session.delete(existing)
                post.likes -= 1
            elif existing.type == "dislike":
                existing.type = "like"
                post.likes += 1
                post.dislikes -= 1
        else:
            new_like = UserLikeDislike(user_id=user.id, post_id=post.id, type="like")
            self.session.add(new_like)
            post.likes += 1
        
        await self.session.commit()
    
    async def dislike_post(self, user: User, post: Post):
        stmt = select(UserLikeDislike).where(
                UserLikeDislike.user_id == user.id, 
                UserLikeDislike.post_id == post.id
            )
        existing = await self.session.scalar(stmt)
        
        if existing:
            if existing.type == "dislike":
                await self.session.delete(existing)
                post.dislikes -= 1
            elif existing.type == "like":
                existing.type = "dislike"
                post.likes -= 1
                post.dislikes += 1
        else:
            new_dislike = UserLikeDislike(user_id=user.id, post_id=post.id, type="dislike")
            self.session.add(new_dislike)
            post.dislikes += 1
        
        await self.session.commit()