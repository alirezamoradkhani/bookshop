from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.user.models import model
from app.user.models.enums import Role

class AuthorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, id:int):
        new_user = model.Author(id=id)
        self.db.add(new_user)
        return new_user
    async def get_by_id(self,id:int):
        result = await self.db.execute(select(model.Author).where(model.Author.id == id))
        return result.scalar_one_or_none()
    
    async def search(self,id = None,name = None):
        query = select(model.BaseUser).where(model.BaseUser.role == Role.AUTHOR)
        if id:
            query = query.where(model.BaseUser.id == id)
        if name:
            query = query.where(model.BaseUser.username.like(f"%{name}%"))
        
        result = await self.db.execute(query)
        return result.scalars().all()