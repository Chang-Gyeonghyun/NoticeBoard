from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

async def paginated_query(query, pageNo: int, pageSize: int, db: AsyncSession):
    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total_count = total_result.scalar()
    
    offset = (pageNo - 1) * pageSize
    paginated_query = query.offset(offset).limit(pageSize)
    
    results = await db.execute(paginated_query)
    items = results.scalars().unique().all()
    
    total_page = (total_count + pageSize - 1) // pageSize if pageSize > 0 else 1
    
    return items, total_page