from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_database
from app.schemas import user
from app.models.models import User

class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session
               
    async def create_user(self, user_form: user.UserSignup) -> User:
        new_user = User(
            userID=user_form.userID,
            password=user_form.password,
            email=user_form.email,
            userName=user_form.userName,
            phone=user_form.phone,
            birthday=user_form.birthday,
            address=user_form.address,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
    
    async def search_user_by_id(self, userID: str) -> User | None:
        user = await self.session.scalar(
            select(User).where(User.userID == userID)
        )
        return user
    async def update_user(self, user: User, update_request: user.UserUpdate):
        for field, value in update_request.dict(exclude_unset=True).items():
            setattr(user, field, value)
            
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user