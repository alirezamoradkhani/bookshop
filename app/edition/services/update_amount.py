from fastapi import HTTPException
from app.user.models.enums import Role

from app.unit_of_work import UnitOfWork

async def update_amount(uow:UnitOfWork,token_data:dict, new_amount:int,edition_id:int):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise HTTPException(status_code=400, detail="Invalid token user")
        
        if current_user.role == Role.USER:
            raise HTTPException(status_code=400, detail="User does not have permission to add editions.")
        
        edition = await uow.edition.get_by_id(edition_id)
        if not edition:
            raise HTTPException(status_code=404, detail="Edition not found")
        if current_user.role == Role.AUTHOR:
            bookauthor = await uow.bookauthor.get_by_authorid_and_bookid(
                book_id=edition.book_id,
                author_id=current_user.id
            )
            if bookauthor is None:
                raise HTTPException(status_code=403, detail="You are not the author of this book")
        if new_amount < 0:
            raise HTTPException(status_code=400, detail="Amount cannot be negative")
        edition.amount = new_amount
    return edition