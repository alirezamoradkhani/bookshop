from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, engine
from app import models, schemas, crud
from app.security import  get_current_user
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def test():
    return "hello"
#user crud
@app.post("/users/singin",response_model= str)
async def verify_email(email: str, db: AsyncSession = Depends(get_db)):
    return await crud.singin(email=email, db=db)

@app.post("/users/create", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, otp: str, db: AsyncSession = Depends(get_db)):
    db_user = await crud.create_user(db=db, otp=otp, user=user)
    return db_user

@app.post("/users/register")
async def login_step_one(user: schemas.UserLogin,db=Depends(get_db)):
    return await crud.login_step_one(db=db,user=user)

@app.post("/users/login", response_model=schemas.TokenResponse)
async def login(email:str,otp :str, db: AsyncSession = Depends(get_db)):
    return await crud.login_step_two(email=email,otp=otp, db=db)

@app.get("/users/all", response_model=list[schemas.UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db), token_data: dict = Depends(get_current_user)):
    return await crud.get_all_users(db=db, token_data=token_data)

@app.get("/users/authors", response_model=list[schemas.UserResponse])
async def get_authors(db: AsyncSession = Depends(get_db)):
    return await crud.get_authors(db=db)

@app.patch("/user/plan")
async def upgrade_plan(new_plan: models.UserPlan,token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.upgrade_plan(db=db,token_data=token_data,new_plan=new_plan)

@app.delete("/users")
async def remove_user(user_id: int, token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.remove_user(db=db, token_data=token_data, user_id=user_id)

#books crud
@app.post("/books", response_model=schemas.BookResponse)
async def add_book(book: schemas.BookCreate, token_data: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.add_book(db=db, token_data=token_data, book=book)

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