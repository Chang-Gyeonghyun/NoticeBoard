from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_database
from app.models.models import Attachment
from fastapi import Depends


class AttachmentRepository:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session
        
    async def save_files(self, post_id, file_urls: list, file_name: list):
        for url, file in zip(file_urls, file_name):
            attachment = Attachment(post_id=post_id, file_path=url, file_name=file)
            self.session.add(attachment)
        await self.session.commit()



    async def get_file_by_id(self, attachment_id: int) -> Attachment | None:
        stmt = select(Attachment).where(Attachment.id == attachment_id)
        result = await self.session.execute(stmt)
        attachment = result.scalars().first()
        
        return attachment