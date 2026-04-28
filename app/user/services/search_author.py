from app.unit_of_work import UnitOfWork
from app.user.schemas.inputs import SearchAuthor

async def search_author(uow:UnitOfWork, name:str|None=None,id:int|None=None):
    return await uow.author.search(id=id,name=name)