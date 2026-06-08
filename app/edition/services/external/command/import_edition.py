from app.edition.models import model
from app.user.models.enums import Role
from app.exceptions.models.user import InvalidTokenUser,OnlyAuthorPrimition,UserPermissionDenied
from app.exceptions.models.book import BookNotFound
from app.exceptions.models.external_service import ExternalServiceCanNotFound, LanguageNotSuported

from app.external_API.providers.open_library.service import OpenLibraryProvider
from app.core.unit_of_work import UnitOfWork

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
        if internal_book.external_id is not None:
            external_editions = [
                e for e in external_editions
                if e.ext_book_id == internal_book.external_id
            ]
            if not external_editions:
                raise ExternalServiceCanNotFound
        else:
            external_editions = [
                e for e in external_editions
                if e.title == external_edition_title
            ]
            if not external_editions:
                raise UserPermissionDenied

        external_edition = external_editions[0]
        if current_user.username not in external_edition.authors:
            raise UserPermissionDenied
        
        ext_book = await provider.get_work(work_id=external_edition.ext_book_id)
        
        new_edition = model.Edition(
            book_id=internal_book.id
            ,price=0
            ,amount = 0
            ,specefic_edition_title = "imported"
            ,isbn = external_edition.isbn
            ,description = ext_book.description
            )
        await uow.edition.create_edition(new_edition)
        await uow.flush()
        for language in external_edition.language:
            new_edition_language = model.EditionLanguage(edition_id = new_edition.id, language = language)
            await uow.editionlanguage.create(new_edition_language)
        return new_edition