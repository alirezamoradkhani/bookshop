from app.edition.models import model
from app.edition.schemas.inputs import EditionCreate
from app.user.models.enums import Role
from app.exceptions.models.user import InvalidTokenUser,OnlyAuthorPrimition,UserPermissionDenied
from app.exceptions.models.book import BookNotFound
from app.exceptions.models.edition import InvalidPrice, InvalidAmount

from app.unit_of_work import UnitOfWork

async def create_edition(uow:UnitOfWork,edition:EditionCreate,token_data:dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        
        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition
        
        book = await uow.book.get_by_id(edition.book_id)

        if book is None:
            raise BookNotFound
        
        if current_user.role == Role.AUTHOR:
            if await uow.bookauthor.get_by_authorid_and_bookid(book_id=book.id,author_id=current_user.id) == None:
                raise UserPermissionDenied
            
        if edition.amount is not None and edition.amount < 0:
            raise InvalidAmount

        if edition.price < 0:
            raise InvalidPrice
        new_edition = model.Edition(
            book_id=edition.book_id
            ,price=edition.price
            ,amount = edition.amount
            ,language=edition.language
            ,specefic_edition_title = edition.specefic_edition_title)
        await uow.edition.create_edition(new_edition)
        await uow.flush()
        return new_edition