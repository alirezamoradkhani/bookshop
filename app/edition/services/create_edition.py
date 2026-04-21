from fastapi import HTTPException
from app.edition.models import model
import app.book.schemas.inputs as inputs
from app.edition.models.enums import Language
from app.edition.schemas.inputs import EditionCreate
from app.user.models.enums import Role

from app.unit_of_work import UnitOfWork

async def create_edition(uow:UnitOfWork,edition:EditionCreate,token_data:dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise HTTPException(status_code=400, detail="Invalid token user")
        
        if current_user.role == Role.USER:
            raise HTTPException(status_code=400, detail="User does not have permission to add editions.")
        
        book = await uow.book.get_by_id(edition.book_id)

        if book is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        
        if current_user.role == Role.AUTHOR:
            if await uow.bookauthor.get_by_authorid_and_bookid(book_id=book.id,author_id=current_user.id) == None:
                raise HTTPException(status_code=403, detail="you are not the author of this book")
            
        if edition.amount is not None and edition.amount < 0:
            raise HTTPException(status_code=400, detail="amount cannot be negative")

        if edition.price < 0:
            raise HTTPException(status_code=400, detail="price cannot be negative")
        new_edition = model.Edition(
            book_id=edition.book_id
            ,price=edition.price
            ,amount = edition.amount
            ,language=edition.language
            ,specefic_edition_title = edition.specefic_edition_title)
        await uow.edition.create_edition(new_edition)
        await uow.flush()
        return new_edition