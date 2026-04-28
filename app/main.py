from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, engine
from app import models, schemas, crud
from app.security import  get_current_user
# models.Base.metadata.create_all(bind=engine)
from app.get_unit_of_work import get_uow
import app.user.schemas.outputs as output
import app.user.schemas.inputs as inputs
from app.user.services.create_baseuser import email_register, create_user
from app.user.services.authenticate import athenticate,verify_email
from app.api.router import api_router
from app.workers.scheduler import scheduler
from app.exceptions.base import DomainException
from app.exceptions.exception_handler import domain_exception_handler


app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(api_router)
app.add_exception_handler(DomainException,domain_exception_handler)

@app.on_event("startup")
async def startup():
    scheduler.start()



@app.get("/")
async def test():
    return "hello"
#user crud

@app.get("/users/all", response_model=list[schemas.UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db), token_data: dict = Depends(get_current_user)):
    return await crud.get_all_users(db=db, token_data=token_data)

#edition crud

#orders crud
    

@app.get("/borrow/overdue")
async def user_with_over_due(db = Depends(get_db)):
    return await crud.user_with_over_due(db=db)

#records

# @app.get("/record/authors/number-of-sell")
# async def best_author_in_sell(db = Depends(get_db)):
#     return await crud.best_author_in_sell(db=db)

# @app.get("/record/authors/total-income")
# async def best_author_in_income(db = Depends(get_db)):
#     return await crud.best_author_in_income(db=db)

# @app.get("/record/editions/number-of-sell")
# async def best_edition_in_sell(db = Depends(get_db)):
#     return await crud.best_edition_in_sell(db=db)

@app.get("/record/editions/number-of-borrow")
async def best_edition_in_borrow(db = Depends(get_db)):
    return await crud.best_edition_in_borrow(db=db)

@app.get("/record/category")
async def best_category_in_sell(db= Depends(get_db)):
    return await crud.best_category_in_sell(db=db)

@app.get("record/author/monthly-income")
async def monthly_income(token_data = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.monthly_income(db=db,token_data=token_data)

@app.get("/record/user/number-of-buy")
async def best_user_in_buy(db: AsyncSession = Depends(get_db)):
    return await crud.best_user_in_buy(db=db)