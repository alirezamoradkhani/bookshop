from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, engine
from app import models, schemas, crud, scheduler
from app.security import  get_current_user
# models.Base.metadata.create_all(bind=engine)
from app.get_unit_of_work import get_uow
import app.user.schemas.outputs as output
import app.user.schemas.inputs as inputs
from app.user.services.create_baseuser import email_register, create_user
from app.user.services.authenticate import athenticate,verify_email
from app.api.router import api_router


app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(api_router)

@app.on_event("startup")
async def startup():
    scheduler.scheduler.start()



@app.get("/")
async def test():
    return "hello"
#user crud

@app.get("/users/all", response_model=list[schemas.UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db), token_data: dict = Depends(get_current_user)):
    return await crud.get_all_users(db=db, token_data=token_data)

@app.get("/users/authors")
async def get_authors(db: AsyncSession = Depends(get_db)):
    return await crud.get_authors(db=db)

# @app.patch("/user/plan")
# async def upgrade_plan(new_plan: models.UserPlan,token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
#     return await crud.upgrade_plan(db=db,token_data=token_data,new_plan=new_plan)

# @app.delete("/users")
# async def remove_user(user_id: int, token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
#     return await crud.remove_user(db=db, token_data=token_data, user_id=user_id)

#books crud
# @app.post("/books")
# async def add_book(book: schemas.BookCreate, token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
#     return await crud.add_book(db=db, token_data=token_data, book=book)

@app.get("/books", response_model=list[schemas.BookResponse])
async def search_books(
    title: str | None = Query(None),
    autho: str | None = Query(None),
    id: int | None = Query(None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await crud.search_books(db=db, title=title, author=autho, id=id, limit=limit, offset=offset)
    

@app.delete("/books")
async def remove_book(book_id: int, token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.remove_book(db=db, token_data=token_data, book_id=book_id)

@app.patch("/books", response_model=schemas.BookResponse)
async def update_book(book_id: int, book: schemas.BookUpdate, token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.update_book(db=db, token_data=token_data, book_id=book_id, book_update=book)

#edition crud
@app.post("/editions")
async def add_edition(edition: schemas.EditionCreate,token_data = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.add_edition(db=db,token_data=token_data,edition=edition)

#orders crud
@app.post("/orders", response_model= schemas.OrderResponse)
async def buy_edition(edition_ids : list[int],token_data = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.buy(db=db, edition_ids=edition_ids, token_data=token_data)

    
@app.patch("/orders", response_model=schemas.OrderResponse)
async def update_order_state(order_id: int, new_state: schemas.OrderState, token_data = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.update_order_state(db=db, order_id=order_id, new_state=new_state, token_data=token_data)

@app.patch("/order/author")
async def update_order_edition_state(order_id: int,edition_id: int,new_state: schemas.OrderItemState, token_data = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.update_order_edition_state(db=db,token_data=token_data,edition_id=edition_id,order_id=order_id,new_state=new_state)

@app.get("/orders")
async def get_order(order_id: int, token_data = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.get_order(db=db, token_data=token_data)

@app.get("/wallet/info")
async def get_wallet_info(token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.wallet_info(token_data=token_data, db=db)

@app.post("/wallet/recharge")
async def recharge_wallet(amount: int, token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.deposit(token_data=token_data, amount=amount, db=db)

@app.post("/wallet/withdraw")
async def withdraw_wallet(amount: int, token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.withdraw_wallet_amount(token_data=token_data, amount=amount, db=db)
@app.post("/wallet/transfer")
async def transfer_funds(recipient_email: str, amount: int, token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.transfer_wallet_amount(token_data=token_data, recipient_email=recipient_email, amount=amount, db=db)

#borrows

@app.post("/borrows/take")
async def borrow_edition(edition_id: int, token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.borrow_edition(db=db,token_data=token_data,edition_id=edition_id)

@app.post("/borrow/return")
async def return_borrow(borrow_id:int, token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.return_borrow(db=db,token_data=token_data,borrow_id=borrow_id)

@app.post("/borrow/waitlist")
async def add_to_waitlist(edition_id: int, token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.add_to_waitlist(db=db,token_data=token_data,edition_id=edition_id)

@app.get("/borrow/overdue")
async def user_with_over_due(db = Depends(get_db)):
    return await crud.user_with_over_due(db=db)

#records

@app.get("/record/authors/number-of-sell")
async def best_author_in_sell(db = Depends(get_db)):
    return await crud.best_author_in_sell(db=db)

@app.get("/record/authors/total-income")
async def best_author_in_income(db = Depends(get_db)):
    return await crud.best_author_in_income(db=db)

@app.get("/record/editions/number-of-sell")
async def best_edition_in_sell(db = Depends(get_db)):
    return await crud.best_edition_in_sell(db=db)

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

# async def create_user_usecase(user: CreateUserRequest, uow):
#     new_user = User(**user)
#     created_user = await uow.user_repo.create(new_user)
#     await uow.flush()
#     return created_user

# @app.post()
# async def create_user(user: CreateUserRequest, uow: Depends(get_uow)):
#     async with uow:
#         user = await create_user_usecase(user)
#         await uow.commit()
#         return user