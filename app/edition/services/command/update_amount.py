from app.user.models.enums import Role
from app.exceptions.models.user import InvalidTokenUser,OnlyAuthorPrimition,UserPermissionDenied
from app.exceptions.models.edition import EditionNotFound,InvalidAmount

from app.unit_of_work import UnitOfWork

async def update_amount(uow:UnitOfWork,token_data:dict, new_amount:int,edition_id:int):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        
        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition
        
        edition = await uow.edition.get_by_id(edition_id)
        if not edition:
            raise EditionNotFound
        if current_user.role == Role.AUTHOR:
            bookauthor = await uow.bookauthor.get_by_authorid_and_bookid(
                book_id=edition.book_id,
                author_id=current_user.id
            )
            if bookauthor is None:
                raise UserPermissionDenied
        if new_amount < 0:
            raise InvalidAmount
        edition.amount = new_amount
    return edition