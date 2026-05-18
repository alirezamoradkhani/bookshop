from fastapi import APIRouter, Depends, Request
from app.core.security import get_current_user
from app.external_API.providers.open_library.get_extternal_services import get_openlibrary_provider
from app.edition.schemas.inputs import EditionCreate
from app.edition.services.command.create_edition import create_edition
from app.edition.services.command.update_amount import update_amount
from app.edition.services.command.update_price import update_price
from app.edition.services.command.delete_edition import remove_edition
from app.edition.services.external.command.import_edition import import_edition
from app.ratelimiter.limiter import limiter
from app.dependency_injection.container import Container
from dependency_injector.wiring import inject, Provide

router = APIRouter(prefix="/editions", tags=["editions"])

@router.post("/")
@limiter.limit("5/minute")
@inject
async def add_edition(request: Request, edition: EditionCreate,uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await create_edition(uow=uow,token_data=token_data,edition=edition)

@router.patch("/amount")
@limiter.limit("5/minute")
@inject
async def change_amount(request: Request, new_amount: int,edition_id : int,uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await update_amount(uow=uow,token_data=token_data,new_amount=new_amount,edition_id=edition_id)

@router.patch("/price")
@limiter.limit("5/minute")
@inject
async def change_price(request: Request, new_price: int,edition_id : int,uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await update_price(uow=uow,token_data=token_data,new_price=new_price,edition_id=edition_id)

@router.delete("/delete")
@limiter.limit("5/minute")
@inject
async def delete_edition(request: Request, edition_id : int,uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user)):
    return await remove_edition(uow=uow,token_data=token_data,edition_id=edition_id)

@router.post("/external")
@limiter.limit("5/minute")
@inject
async def Import_edition(request: Request, book_id: int,external_edition_title:str,uow = Depends(Provide[Container.uow]),token_data = Depends(get_current_user),provider = Depends(Provide[Container.openlibrary])):
    return await import_edition(uow=uow,token_data=token_data,book_id=book_id,external_edition_title=external_edition_title,provider=provider)