from fastapi import APIRouter, Depends
from app.get_unit_of_work import get_uow
from app.analytics.service.author.best_author_in_sell import best_author_in_sell
from app.analytics.service.author.best_author_in_income import best_author_in_income
from app.analytics.service.edition.best_edition_in_sell import best_edition_in_sell

router = APIRouter(prefix="/records", tags=["records"])



@router.get("/author/best_in_sell")
async def author_in_sell(uow=Depends(get_uow)):
    return await best_author_in_sell(uow=uow)

@router.get("/author/best_in_total_income")
async def author_in_income(uow=Depends(get_uow)):
    return await best_author_in_income(uow=uow)

@router.get("/edition/number_of_sell")
async def edition_in_sell(uow=Depends(get_uow)):
    return await best_edition_in_sell(uow=uow)