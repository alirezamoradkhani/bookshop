from app.edition.models import model
from app.edition.schemas.inputs import EditionCreate
from app.user.models.enums import Role
from app.exceptions.models.user import InvalidTokenUser,OnlyAuthorPrimition,UserPermissionDenied
from app.exceptions.models.book import BookNotFound
from app.exceptions.models.edition import InvalidPrice, InvalidAmount
from app.exceptions.models.external_service import ExternalServiceCanNotFound, LanguageNotSuported

from app.external_API.providers.open_library.service import OpenLibraryProvider
from app.unit_of_work import UnitOfWork

async def import_edition(uow:UnitOfWork,provider:OpenLibraryProvider,book_id:int,external_edition_title:str,token_data:dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        
        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition
        internal_book = await uow.book.get_by_id(book_id)
        if internal_book is None:
            raise BookNotFound
        
        if current_user.role == Role.AUTHOR:
            if await uow.bookauthor.get_by_authorid_and_bookid(book_id=internal_book.id,author_id=current_user.id) == None:
                raise UserPermissionDenied
            
        external_editions = await provider.search_by_title(external_edition_title)
        if external_editions == []:
            raise ExternalServiceCanNotFound
        external_edition = external_editions[0]
        if current_user.username not in external_edition.authors:
            raise UserPermissionDenied
        if "eng" in external_edition.language:
            language = "en"
        elif "per" in external_edition.language:
            language = "fa"
        elif "ara" in external_edition.language:
            language = "arb"
        else:
            raise LanguageNotSuported
        new_edition = model.Edition(
            book_id=internal_book.id
            ,price=0
            ,amount = 0
            ,language=language
            ,specefic_edition_title = "imported"
            )
        await uow.edition.create_edition(new_edition)
        await uow.flush()
        return new_edition