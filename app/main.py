from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import get_db, engine
import models, schemas, crud
from security import  get_current_user
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def test():
    return "hello"
#user crud
@app.post("/users/singin",response_model= str)
def verify_email(email: str, db: Session = Depends(get_db)):
    return crud.singin(email=email, db=db)

@app.post("/users/create", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, otp: str, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, otp=otp, user=user)
    return db_user

@app.post("/users/register")
def login_step_one(user: schemas.UserLogin,db=Depends(get_db)):
    return crud.login_step_one(db=db,user=user)

@app.post("/users/login", response_model=schemas.TokenResponse)
def login(email:str,otp :str, db: Session = Depends(get_db)):
    return crud.login_step_two(email=email,otp=otp, db=db)

@app.get("/users/all", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db), token_data: dict = Depends(get_current_user)):
    return crud.get_all_users(db=db, token_data=token_data)

@app.get("/users/authors", response_model=list[schemas.UserResponse])
def get_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db=db)
@app.delete("/users")
def remove_user(user_id: int, token_data: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.remove_user(db=db, token_data=token_data, user_id=user_id)

#books crud
@app.post("/books", response_model=schemas.BookResponse)
def add_book(book: schemas.BookCreate, token_data: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.add_book(db=db, token_data=token_data, book=book)

@app.get("/books", response_model=list[schemas.BookResponse])
def search_books(
    title: str | None = Query(None),
    autho: str | None = Query(None),
    id: int | None = Query(None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return crud.search_books(db=db, title=title, author=autho, id=id, limit=limit, offset=offset)
    

@app.delete("/books")
def remove_book(book_id: int, token_data: dict = Depends(get_current_user), db=Depends(get_db)):
    return crud.remove_book(db=db, token_data=token_data, book_id=book_id)

@app.patch("/books", response_model=schemas.BookResponse)
def update_book(book_id: int, book: schemas.BookUpdate, token_data: dict = Depends(get_current_user), db=Depends(get_db)):
    return crud.update_book(db=db, token_data=token_data, book_id=book_id, book=book)
#orders crud
@app.post("/orders", response_model= schemas.OrderResponse)
def buy_book(book_id : int,token_data = Depends(get_current_user), db = Depends(get_db)):
    return crud.buy(db=db, book_id=book_id, token_data=token_data)


@app.patch("/orders", response_model=schemas.OrderResponse)
def update_order_state(order_id: int, new_state: schemas.OrderState, token_data = Depends(get_current_user), db = Depends(get_db)):
    return crud.update_order_state(db=db, order_id=order_id, new_state=new_state.value, token_data=token_data)


@app.get("/orders")
def get_order(order_id: int, token_data = Depends(get_current_user), db = Depends(get_db)):
    return crud.get_order(db=db, order_id=order_id, token_data=token_data)

@app.get("/wallet/info")
def get_wallet_info(token_data: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_wallet_info(token_data=token_data, db=db)

@app.post("/wallet/recharge")
def recharge_wallet(amount: int, token_data: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.deposit(token_data=token_data, amount=amount, db=db)

@app.post("/wallet/withdraw")
def withdraw_wallet(amount: int, token_data: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.withdraw(token_data=token_data, amount=amount, db=db)
@app.post("/wallet/transfer")
def transfer_funds(recipient_email: str, amount: int, token_data: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.transfer_funds(token_data=token_data, recipient_email=recipient_email, amount=amount, db=db)