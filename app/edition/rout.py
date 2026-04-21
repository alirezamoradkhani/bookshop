from fastapi import APIRouter, Depends
from app.security import get_current_user
from app.get_unit_of_work import get_uow
from app.edition.schemas.inputs import EditionCreate
from app.edition.services.create_edition import create_edition


router = APIRouter(prefix="/editions", tags=["editions"])

@router.post("/create")
async def add_edition(edition: EditionCreate,uow = Depends(get_uow),token_data = Depends(get_current_user)):
    return await create_edition(uow=uow,token_data=token_data,edition=edition)