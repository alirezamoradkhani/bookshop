from security import create_access_token, hash_password, verify_password, redis_client
from otp import send_otp, verify_otp
from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
import schemas
import datetime
    

def singin(email: str,db: Session):
    db_user = db.query(models.BaseUser).filter(models.BaseUser.email == email).first()
    if db_user is not None:
        raise HTTPException(status_code=400, detail="email already registered")
    send_otp(email)
    return "OTP sent to email"

def create_user(db: Session, otp: str, user: schemas.UserCreate):
    if not verify_otp(user.email, otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    if user.role not in [models.Role.USER.value, models.Role.AUTHOR.value]:
        raise HTTPException(status_code=400, detail="Invalid role")
    hashed_password = hash_password(user.password)
    new_user = models.BaseUser(username=user.username, email=user.email, password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def remove_user(db: Session, token_data: dict, user_id: int):
    current_user = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role != models.Role.ADMIN:
        raise HTTPException(status_code=400, detail="Only admin users can remove users.")
    user_to_remove = db.query(models.BaseUser).filter(models.BaseUser.id == user_id).first()
    if user_to_remove is None:
        raise HTTPException(status_code=404, detail="User not found.")
    db.delete(user_to_remove)
    db.commit()

def login_step_one(db: Session, user: schemas.UserLogin):
    user_in_db = db.query(models.BaseUser).filter(models.BaseUser.username == user.username).first()
    if user_in_db is None or not verify_password(user.password, user_in_db.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    send_otp(user_in_db.email)
    return "OTP sent to email"

def login_step_two(db: Session, email: str, otp: str):
    if not verify_otp(email, otp):
        raise Exception("Invalid OTP")
    user = db.query(models.BaseUser).filter(models.BaseUser.email == email).first()
    if user is None:
        raise Exception("Invalid email or password")
    token_data = {
        "user_id": user.id,
    }
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

def get_all_users(db: Session, token_data: dict):
    db_user = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if db_user.role != models.Role.ADMIN.value:
        raise HTTPException(status_code=400, detail="Only admin users can access this resource.")
    return db.query(models.BaseUser).all()

def get_authors(db: Session):
    return db.query(models.Author).all()

def add_book(db: Session, token_data: dict, book: schemas.BookCreate):
    current_user = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role == models.Role.USER:
        raise HTTPException(status_code=400, detail="User does not have permission to add books.")
    if current_user.role == models.Role.AUTHOR:
        db_book = models.Book(title=book.title, price=book.price, amount=book.amount)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        book_author = models.BookAuthor(book_id=db_book.id, authors_id=current_user.id)
        db.add(book_author)
        db.commit()
        return db_book
        
def remove_book(db: Session, token_data: dict, book_id: int):
    current_user = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role == models.Role.USER:
        raise HTTPException(status_code=400, detail="User does not have permission to remove books.")
    if current_user.role == models.Role.AUTHOR:
        book = db.query(models.Book).filter(models.Book.id == book_id, models.Book.author_id == current_user.id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found or you do not have permission to remove this book.")
        db.delete(book)
        db.commit()
    elif current_user.role == models.Role.ADMIN:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        db.delete(book)
        db.commit()

def update_book(db: Session, token_data: dict, book_id: int, book_update: schemas.BookUpdate):
    current_user = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role == models.Role.USER:
        raise HTTPException(status_code=400, detail="User does not have permission to update books.")

    if current_user.role == models.Role.AUTHOR:
        book = db.query(models.Book).filter(models.Book.id == book_id, models.Book.author_id == current_user.id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found or you do not have permission to update this book.")
        book.title = book_update.title
        book.amount = book_update.amount
        book.price = book_update.price
        db.commit()
        db.refresh(book)
        return book

    if current_user.role == models.Role.ADMIN:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        book.title = book_update.title
        book.amount = book_update.amount
        book.price = book_update.price
        db.commit()
        db.refresh(book)
        return book

def search_books(db: Session, title: str | None = None, author: str | None = None, id: int | None = None, limit: int = 10, offset: int = 0):
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        authors = db.query(models.Author).filter(models.Author.username.ilike(f"%{author}%")).all()
        author_ids = [author.id for author in authors]
        query = query.join(models.BookAuthor).filter(models.BookAuthor.author_id.in_(author_ids))
    if id is not None:
        query = query.filter(models.Book.id == id)
    return query.offset(offset).limit(limit).all()

def buy(db: Session, book_ids: list, token_data: dict):
    current_user = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role != models.Role.USER:
        raise HTTPException(status_code=400, detail="Only users can buy books.")
    final_price = 0
    for book_id in book_ids:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        if book.amount <= 0:
            raise HTTPException(status_code=400, detail="Book is out of stock.")
        final_price += book.price
    if current_user.wallet_amount < final_price:
        raise HTTPException(status_code=400, detail="Insufficient funds in wallet.")
    current_user.wallet_amount -= final_price
    for book_id in book_ids:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        book.amount -= 1
    new_order = models.Order(customer_id=current_user.id, state=schemas.OrderState.WAITFORSELLER.value, final_price=final_price, date=str(datetime.utcnow()))
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    order_book = models.ordersbooks(order_id=new_order.id, book_id=book.id)
    db.add(order_book)
    db.commit()
    return new_order

def get_order(db: Session,token_data: dict):
    current_user = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role == models.Role.USER:
        orders = db.query(models.ordersbooks).join(models.Order).filter(models.Order.customer_id == current_user.id).all()
    elif current_user.role == models.Role.AUTHOR:
        author_books = db.query(models.BookAuthor).filter(models.BookAuthor.author_id == current_user.id).all()
        book_ids = [book.book_id for book in author_books]
        orders = db.query(models.ordersbooks).join(models.Order).filter(models.ordersbooks.book_id.in_(book_ids)).all()
    elif current_user.role == models.Role.ADMIN:
        orders = db.query(models.ordersbooks).join(models.Order).all()
    return orders

def update_order_state(db: Session, token_data: dict, order_id: int, new_state: schemas.OrderState):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    current_user = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if order.state == schemas.OrderState.CANCELED.value or order.state == schemas.OrderState.DONE.value:
        raise HTTPException(status_code=400, detail="Cannot update a completed or canceled order.")
    else:
        if current_user.role == models.Role.USER:
            if order.customer_id != current_user.id:
                raise HTTPException(status_code=403, detail="You do not have permission to update this order.")
            if new_state == schemas.OrderState.CANCELED:
                order.state = new_state.value
                current_user.wallet_amount += order.final_price
                for book_id in book_ids:
                    book = db.query(models.Book).filter(models.Book.id == book_id).first()
                    book.amount += 1
                db.commit()
                return order
            else:
                raise HTTPException(status_code=400, detail="Users can only cancel their orders.")
        elif current_user.role == models.Role.AUTHOR:
            author_books = db.query(models.BookAuthor).filter(models.BookAuthor.author_id == current_user.id).all()
            book_ids = [book.book_id for book in author_books]
            order_book = db.query(models.ordersbooks).filter(models.ordersbooks.order_id == order_id, models.ordersbooks.book_id.in_(book_ids)).first()
            if order_book is None:
                raise HTTPException(status_code=403, detail="You do not have permission to update this order.")
            if new_state == schemas.OrderState.INPROCCES:
                order.state = new_state.value
                current_user.wallet_amount += order.final_price * 0.95
                db.commit()
                return order
            else:
                raise HTTPException(status_code=400, detail="Authors can only mark orders as in process or done.")
    if current_user.role == models.Role.ADMIN:
        order.state = new_state.value
        db.commit()
        return order
    
def increase_wallet_amount(db: Session, token_data: dict, amount: int):
    current_user = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role != models.Role.USER:
        raise HTTPException(status_code=400, detail="Only users can increase wallet amount.")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
    current_user.wallet_amount += amount
    transfer = models.transaction(user_id=current_user.id, amount=amount, type=models.transactionType.DEPOSIT.value, date=str(datetime.utcnow()))
    db.add(transfer)
    db.commit()
    return current_user.wallet_amount

def transfer_wallet_amount(db: Session, token_data: dict, recipient_email: str, amount: int):
    sender = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if sender is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if sender.role != models.Role.USER:
        raise HTTPException(status_code=400, detail="Only users can transfer wallet amount.")
    recipient = db.query(models.BaseUser).filter(models.BaseUser.email == recipient_email).first()
    if recipient is None:
        raise HTTPException(status_code=404, detail="Recipient not found.")
    if recipient.role != models.Role.USER:
        raise HTTPException(status_code=400, detail="Recipient must be a user.")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
    if sender.wallet_amount < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds in wallet.")
    sender.wallet_amount -= amount
    recipient.wallet_amount += amount
    sender_transaction = models.transaction(user_id=sender.id, amount=amount, type=models.transactionType.SEND.value, date=str(datetime.utcnow()))
    recipient_transaction = models.transaction(user_id=recipient.id, amount=amount, type=models.transactionType.RECEIVE.value, date=str(datetime.utcnow()))
    db.add(sender_transaction)
    db.add(recipient_transaction)
    db.commit()
    return {"sender_wallet_amount": sender.wallet_amount, "recipient_wallet_amount": recipient.wallet_amount}

def deposit(token_data: dict, amount: int, db: Session):
    current_user = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role != models.Role.USER:
        raise HTTPException(status_code=400, detail="Only users can deposit to wallet.")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
    # Simulate deposit confirmation (e.g., through a payment gateway)
    # In a real application, you would integrate with a payment gateway and confirm the payment before updating the wallet amount.
    current_user.wallet_amount += amount
    transfer = models.transaction(user_id=current_user.id, amount=amount, type=models.transactionType.DEPOSIT.value, date=str(datetime.utcnow()))
    db.add(transfer)
    db.commit()

def confirm_deposit(token_data: dict, amount: int, db: Session):
    ...
    
def withdraw_wallet_amount(db: Session, token_data: dict, amount: int):
    current_user = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role != models.Role.AUTHOR:
        raise HTTPException(status_code=400, detail="Only authors can withdraw from wallet.")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
    if current_user.wallet_amount < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds in wallet.")
    current_user.wallet_amount -= amount
    transfer = models.transaction(user_id=current_user.id, amount=amount, type=models.transactionType.WITHDRAWAL.value, date=str(datetime.utcnow()))
    db.add(transfer)
    db.commit()
    return current_user.wallet_amount

def wallet_info(db: Session, token_data: dict):
    current_user = db.query(models.BaseUser).filter(models.BaseUser.id == token_data["user_id"]).first()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    transactions = db.query(models.transaction).filter(models.transaction.user_id == current_user.id).all()
    transactions_data = []
    for transaction in transactions:
        transactions_data.append({
            "amount": transaction.amount,
            "type": transaction.type,
            "date": transaction.date
        })
    return {"wallet_amount": current_user.wallet_amount, "transactions": transactions_data}