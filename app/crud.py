from sqlalchemy import select
from app.security import create_access_token, hash_password, verify_password, redis_client
from app.otp import send_otp, verify_otp, create_otp
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app import models
from app import schemas
from datetime import datetime
    

async def singin(email: str,db: AsyncSession):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.email == email, models.BaseUser.delete_time.is_(None)))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="email already registered")
    await create_otp(email)
    return "OTP sent to email"

async def create_user(db: AsyncSession, otp: str, user: schemas.UserCreate):
    if not await verify_otp(user.email, otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    if user.role not in [models.Role.USER.value, models.Role.AUTHOR.value]:
        raise HTTPException(status_code=400, detail="Invalid role")
    hashed_password = hash_password(user.password)
    new_user = models.BaseUser(username=user.username, email=user.email, password=hashed_password, role=user.role)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def remove_user(db: AsyncSession, token_data: dict, user_id: int):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == user_id, models.BaseUser.delete_time.is_(None)))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role != models.Role.ADMIN:
        raise HTTPException(status_code=400, detail="Only admin users can remove users.")
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == user_id, models.BaseUser.delete_time.is_(None)))
    user_to_remove = result.scalar_one_or_none()
    if user_to_remove is None:
        raise HTTPException(status_code=404, detail="User not found.")
    user_to_remove.delete_time = str(datetime.utcnow())
    await db.commit()

async def login_step_one(db: AsyncSession, user: schemas.UserLogin):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.username == user.username, models.BaseUser.delete_time.is_(None)))
    user_in_db = result.scalar_one_or_none()
    if user_in_db is None or not verify_password(user.password, user_in_db.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    await create_otp(user_in_db.email)
    return "OTP sent to email"

async def login_step_two(db: AsyncSession, email: str, otp: str):
    if not await verify_otp(email, otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.email == email, models.BaseUser.delete_time.is_(None)))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    token_data = {
        "user_id": user.id,
    }
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

async def get_all_users(db: AsyncSession, token_data: dict):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.delete_time.is_(None)))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if db_user.role != models.Role.ADMIN.value:
        raise HTTPException(status_code=400, detail="Only admin users can access this resource.")
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.delete_time.is_(None)))
    return result.scalars().all()

async def get_authors(db: AsyncSession):
    result = await db.execute(select(models.Author).where(models.Author.delete_time.is_(None)))
    return result.scalars().all()

async def add_book(db: AsyncSession, token_data: dict, book: schemas.BookCreate):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.delete_time.is_(None)))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role == models.Role.USER:
        raise HTTPException(status_code=400, detail="User does not have permission to add books.")
    if current_user.role == models.Role.AUTHOR:
        db_book = models.Book(title=book.title, price=book.price, amount=book.amount)
        db.add(db_book)
        await db.commit()
        await db.refresh(db_book)
        book_author = models.BookAuthor(book_id=db_book.id, authors_id=current_user.id)
        db.add(book_author)
        await db.commit()
        return db_book
        
async def remove_book(db: AsyncSession, token_data: dict, book_id: int):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.delete_time.is_(None)))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role == models.Role.USER:
        raise HTTPException(status_code=400, detail="User does not have permission to remove books.")
    if current_user.role == models.Role.AUTHOR:
        result = await db.execute(select(models.Book).where(models.Book.id == book_id, models.Book.delete_time.is_(None)))
        book = result.scalar_one_or_none()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found or you do not have permission to remove this book.")
        book.delete_time = str(datetime.utcnow())
        await db.commit()
    elif current_user.role == models.Role.ADMIN:
        result = await db.execute(select(models.Book).where(models.Book.id == book_id, models.Book.delete_time.is_(None)))
        book = result.scalar_one_or_none()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        book.delete_time = str(datetime.utcnow())
        await db.commit()

async def update_book(db: AsyncSession, token_data: dict, book_id: int, book_update: schemas.BookUpdate):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.delete_time.is_(None)))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role == models.Role.USER:
        raise HTTPException(status_code=400, detail="User does not have permission to update books.")

    if current_user.role == models.Role.AUTHOR:
        result = await db.execute(select(models.Book).where(models.Book.id == book_id, models.Book.delete_time.is_(None)))
        book = result.scalar_one_or_none()
        result = await db.execute(select(models.BookAuthor).where(models.BookAuthor.book_id == book_id, models.BookAuthor.authors_id == current_user.id))
        book_author = result.scalar_one_or_none()
        if book_author is None or book is None:
            raise HTTPException(status_code=404, detail="Book not found or you do not have permission to update this book.")
        if book_update.title is not None:
            book.title = book_update.title
        if book_update.amount is not None:
            book.amount = book_update.amount
        if book_update.price is not None:
            book.price = book_update.price
        await db.commit()
        await db.refresh(book)
        return book

    if current_user.role == models.Role.ADMIN:
        result = await db.execute(select(models.Book).where(models.Book.id == book_id, models.Book.delete_time.is_(None)))
        book = result.scalar_one_or_none()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        if book_update.title is not None:
            book.title = book_update.title
        if book_update.amount is not None:
            book.amount = book_update.amount
        if book_update.price is not None:
            book.price = book_update.price
        await db.commit()
        await db.refresh(book)
        return book

from sqlalchemy import select

async def search_books(db: AsyncSession,title: str | None = None,author: str | None = None,id: int | None = None,limit: int = 10, offset: int = 0):
    query = select(models.Book)

    if author:
        query = query.join(models.BookAuthor, models.BookAuthor.book_id == models.Book.id)\
                     .join(models.Author, models.Author.id == models.BookAuthor.author_id)\
                     .where(
                         models.Author.username.ilike(f"%{author}%"),
                         models.Author.delete_time.is_(None),
                         models.Book.delete_time.is_(None)
                     )

    if title:
        query = query.where(
            models.Book.title.ilike(f"%{title}%"),
            models.Book.delete_time.is_(None)
        )

    if id is not None:
        query = query.where(models.Book.id == id)

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()

async def buy(db: AsyncSession, book_ids: list[int], token_data: dict):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.delete_time.is_(None)))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role != models.Role.USER:
        raise HTTPException(status_code=400, detail="Only users can buy books.")
    final_price = 0
    for book_id in book_ids:
        result = await db.execute(select(models.Book).where(models.Book.id == book_id, models.Book.delete_time.is_(None)))
        book = result.scalar_one_or_none()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        if book.amount <= 0:
            raise HTTPException(status_code=400, detail="Book is out of stock.")
        final_price += book.price
    if current_user.wallet_amount < final_price:
        raise HTTPException(status_code=400, detail="Insufficient funds in wallet.")
    current_user.wallet_amount -= final_price
    for book_id in book_ids:
        result = await db.execute(select(models.Book).where(models.Book.id == book_id, models.Book.delete_time.is_(None)))
        book = result.scalar_one_or_none()
        if book is not None:
            book.amount -= 1
    new_order = models.Order(customer_id=current_user.id, state=schemas.OrderState.WAITFORSELLER.value, final_price=final_price, date=str(datetime.utcnow()))
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    for book_id in book_ids:
        order_book = models.ordersbooks(order_id=new_order.id, book_ids=book_id)
        db.add(order_book)
    await db.commit()
    return new_order

async def get_order(db: AsyncSession,token_data: dict):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.delete_time.is_(None)))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role == models.Role.USER:
        result = await db.execute(select(models.ordersbooks).join(models.Order).where(models.Order.customer_id == current_user.id))
        orders = result.scalars().all()
    elif current_user.role == models.Role.AUTHOR:
        result = await db.execute(select(models.BookAuthor).where(models.BookAuthor.author_id == current_user.id))
        author_books = result.scalars().all()
        book_ids = [book.book_id for book in author_books]
        result = await db.execute(select(models.ordersbooks).join(models.Order).where(models.ordersbooks.book_id.in_(book_ids)))
        orders = result.scalars().all()
    elif current_user.role == models.Role.ADMIN:
        result = await db.execute(select(models.ordersbooks).join(models.Order))
        orders = result.scalars().all()
    return orders

async def update_order_state(db: AsyncSession, token_data: dict, order_id: int, new_state: schemas.OrderState):
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.delete_time.is_(None)))
    current_user = result.scalar_one_or_none()
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
                await db.commit()
                return order
            else:
                raise HTTPException(status_code=400, detail="Users can only cancel their orders.")
        elif current_user.role == models.Role.AUTHOR:
            result = await db.execute(select(models.BookAuthor).where(models.BookAuthor.author_id == current_user.id))
            author_books = result.scalars().all()
            book_ids = [book.book_id for book in author_books]
            result = await db.execute(select(models.ordersbooks).where(models.ordersbooks.order_id == order_id, models.ordersbooks.book_id.in_(book_ids)))
            order_book = result.scalar_one_or_none()
            if order_book is None:
                raise HTTPException(status_code=403, detail="You do not have permission to update this order.")
            if new_state == schemas.OrderState.INPROCCES:
                order.state = new_state.value
                current_user.wallet_amount += order.final_price
                await db.commit()
                return order
            else:
                raise HTTPException(status_code=400, detail="Authors can only mark orders as in process or done.")
    
async def increase_wallet_amount(db: AsyncSession, token_data: dict, amount: int):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.delete_time.is_(None)))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role != models.Role.USER:
        raise HTTPException(status_code=400, detail="Only users can increase wallet amount.")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
    current_user.wallet_amount += amount
    transfer = models.transaction(user_id=current_user.id, amount=amount, type=models.transactionType.DEPOSIT.value, date=str(datetime.utcnow()))
    db.add(transfer)
    await db.commit()
    return current_user.wallet_amount

async def transfer_wallet_amount(db: AsyncSession, token_data: dict, recipient_email: str, amount: int):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.delete_time.is_(None)))
    sender = result.scalar_one_or_none()
    if sender is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if sender.role != models.Role.USER:
        raise HTTPException(status_code=400, detail="Only users can transfer wallet amount.")
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.email == recipient_email, models.BaseUser.delete_time.is_(None)))
    recipient = result.scalar_one_or_none()
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
    await db.commit()
    return {"sender_wallet_amount": sender.wallet_amount, "recipient_wallet_amount": recipient.wallet_amount}

async def deposit(token_data: dict, amount: int, db: AsyncSession):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.delete_time.is_(None)))
    current_user = result.scalar_one_or_none()
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
    await db.commit()

async def confirm_deposit(token_data: dict, amount: int, db: AsyncSession):
    ...
    
async def withdraw_wallet_amount(db: AsyncSession, token_data: dict, amount: int):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.delete_time.is_(None)))
    current_user = result.scalar_one_or_none()
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
    await db.commit()
    return current_user.wallet_amount

async def wallet_info(db: AsyncSession, token_data: dict):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.delete_time.is_(None)))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    result = await db.execute(select(models.transaction).where(models.transaction.user_id == current_user.id))
    transactions = result.scalars().all()
    transactions_data = []
    for transaction in transactions:
        transactions_data.append({
            "amount": transaction.amount,
            "type": transaction.type,
            "date": transaction.date
        })
    return {"wallet_amount": current_user.wallet_amount, "transactions": transactions_data}