from fastapi import APIRouter, Depends, Request
from app.analytics.service.author.best_author_in_sell import best_author_in_sell
from app.analytics.service.author.best_author_in_income import best_author_in_income
from app.analytics.service.edition.best_edition_in_sell import best_edition_in_sell
from app.analytics.service.edition.best_edition_in_borrow import best_edition_in_borrow
from app.analytics.service.category.best_category_in_sell import best_category_in_sell
from app.analytics.service.user.bast_user_in_buy import best_user_in_buy
from dependency_injector.wiring import inject, Provide
from app.dependency_injection.container import Container
from app.ratelimiter.limiter import limiter
from app.analytics.schemas.outputs import Best_edition_in_borrow

router = APIRouter(prefix="/records", tags=["records"])



@router.get("/author/best_in_sell")
@limiter.limit("5/minute")
@inject
async def author_in_sell(request: Request,uow=Depends(Provide[Container.uow])):
    return await best_author_in_sell(uow=uow)

@router.get("/author/best_in_total_income")
@limiter.limit("5/minute")
@inject
async def author_in_income(request: Request,uow=Depends(Provide[Container.uow])):
    return await best_author_in_income(uow=uow)

@router.get("/edition/best_in_number_of_sell")
@limiter.limit("5/minute")
@inject
async def edition_in_sell(request: Request,uow=Depends(Provide[Container.uow])):
    return await best_edition_in_sell(uow=uow)

@router.get("/edition/best_in_borrow",response_model=list[Best_edition_in_borrow])
@limiter.limit("5/minute")
@inject
async def edition_in_borrow(request: Request,uow=Depends(Provide[Container.uow])):
    return await best_edition_in_borrow(uow=uow)

@router.get("/category/best_in_sales")
@limiter.limit("5/minute")
@inject
async def category_in_borrow(request: Request,uow=Depends(Provide[Container.uow])):
    return await best_category_in_sell(uow=uow)

@router.get("/user/best_in_buy")
@limiter.limit("5/minute")
@inject
async def user_in_buy(request: Request,uow=Depends(Provide[Container.uow])):
    return await best_user_in_buy(uow=uow)