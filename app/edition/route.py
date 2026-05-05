from fastapi import APIRouter, Depends
from app.security import get_current_user
from app.get_unit_of_work import get_uow
from app.external_API.providers.open_library.get_extternal_services import get_openlibrary_provider
from app.edition.schemas.inputs import EditionCreate
from app.edition.services.command.create_edition import create_edition
from app.edition.services.command.update_amount import update_amount
from app.edition.services.command.update_price import update_price
from app.edition.services.command.delete_edition import remove_edition
from app.edition.services.external.command.import_edition import import_edition


router = APIRouter(prefix="/editions", tags=["editions"])

@router.post("/")
async def add_edition(edition: EditionCreate,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await create_edition(uow=uow,token_data=token_data,edition=edition)

@router.patch("/amount")
async def change_amount(new_amount: int,edition_id : int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await update_amount(uow=uow,token_data=token_data,new_amount=new_amount,edition_id=edition_id)

@router.patch("/price")
async def change_price(new_price: int,edition_id : int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await update_price(uow=uow,token_data=token_data,new_price=new_price,edition_id=edition_id)

@router.delete("/delete")
async def delete_edition(edition_id : int,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await remove_edition(uow=uow,token_data=token_data,edition_id=edition_id)

@router.post("/external")
async def Import_edition(book_id: int,external_edition_title:str,uow = Depends(get_uow),token_data = Depends(get_current_user),provider = Depends(get_openlibrary_provider)):
    return await import_edition(uow=uow,token_data=token_data,book_id=book_id,external_edition_title=external_edition_title,provider=provider)