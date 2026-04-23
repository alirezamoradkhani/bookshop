from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,desc
from app.models import *



async def best_edition_in_borrow(db: AsyncSession):
    result = await db.execute(
        select(Book.id,
               Book.title,
               Book.category,
               Edition.id,
               Edition.specefic_edition_title,
               func.count(Borrow.id).label("total_borrow"))
               .join(Edition, Edition.book_id == Book.id)
               .join(Borrow, Borrow.edition_id == Edition.id)
               .group_by(Edition.id,Book.id,Book.category,Book.title,Edition.specefic_edition_title)
               .order_by(desc("total_borrow"))
               .limit(20)
    )
    return result.all()