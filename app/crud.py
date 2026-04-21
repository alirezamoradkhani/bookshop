from sqlalchemy import select, func, update, case, desc, and_
from app.security import create_access_token, hash_password, verify_password, redis_client
from app.otp import send_otp, verify_otp, create_otp
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app import models
from app import schemas
from datetime import datetime, timedelta, timezone
    


async def test(db:AsyncSession):
    result = await db.execute(select(models.BaseUser))
    return result.scalars().all()

# async def singin(email: str,db: AsyncSession):
#     result = await db.execute(select(models.BaseUser).where(models.BaseUser.email == email, models.BaseUser.is_deleted == False))
#     if result.scalar_one_or_none() is not None:
#         raise HTTPException(status_code=400, detail="email already registered")
#     await create_otp(email)
#     return "OTP sent to email"

# async def create_user(db: AsyncSession, otp: str, user: schemas.UserCreate):
#     if not await verify_otp(user.email, otp):
#         raise HTTPException(status_code=400, detail="Invalid OTP")
#     if user.role not in [models.Role.USER.value, models.Role.AUTHOR.value]:
#         raise HTTPException(status_code=400, detail="Invalid role")
#     hashed_password = hash_password(user.password)
#     new_user = models.BaseUser(username=user.username, email=user.email, password=hashed_password, role=user.role)
#     db.add(new_user)
#     await db.flush()
#     if user.role == models.Role.AUTHOR:
#         author = models.Author(id=new_user.id)
#         db.add(author)
#     if user.role == models.Role.USER:
#         user = models.User(id=new_user.id)
#         db.add(user)
#     await db.commit()
#     await db.refresh(new_user)
#     return new_user

# async def create_author(db: AsyncSession, otp: str):
#     ...

# async def remove_user(db: AsyncSession, token_data: dict, user_id: int):
#     result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == user_id, models.BaseUser.is_deleted == False))
#     current_user = result.scalar_one_or_none()
#     if current_user is None:
#         raise HTTPException(status_code=400, detail="Invalid token user")
#     if current_user.role != models.Role.ADMIN:
#         raise HTTPException(status_code=400, detail="Only admin users can remove users.")
#     result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == user_id, models.BaseUser.is_deleted == False))
#     user_to_remove = result.scalar_one_or_none()
#     if user_to_remove is None:
#         raise HTTPException(status_code=404, detail="User not found.")
#     user_to_remove.is_deleted = True
#     await db.commit()

# async def login_step_one(db: AsyncSession, user: schemas.UserLogin):
#     result = await db.execute(select(models.BaseUser).where(models.BaseUser.username == user.username, models.BaseUser.is_deleted == False))
#     user_in_db = result.scalar_one_or_none()
#     if user_in_db is None or not verify_password(user.password, user_in_db.password):
#         raise HTTPException(status_code=400, detail="Invalid username or password")
#     await create_otp(user_in_db.email)
#     return "OTP sent to email"

# async def login_step_two(db: AsyncSession, email: str, otp: str):
#     if not await verify_otp(email, otp):
#         raise HTTPException(status_code=400, detail="Invalid OTP")
#     result = await db.execute(select(models.BaseUser).where(models.BaseUser.email == email, models.BaseUser.is_deleted == False))
#     user = result.scalar_one_or_none()
#     if user is None:
#         raise HTTPException(status_code=400, detail="Invalid email or password")
#     token_data = {
#         "user_id": user.id,
#     }
#     access_token = create_access_token(token_data)
#     return {"access_token": access_token, "token_type": "bearer"}

# async def upgrade_plan(db: AsyncSession, token_data: dict,new_plan: models.UserPlan):
#     result = await db.execute(select(models.User)
#                               .join(models.BaseUser,models.BaseUser.id == models.User.id)
#                               .where(models.User.id == token_data["user_id"], models.BaseUser.is_deleted == False))
#     current_user = result.scalar_one_or_none()
#     if current_user is None:
#         raise HTTPException(status_code=400, detail="Invalid token user")
#     current_user.plan = new_plan
#     await db.commit()
#     return "ok"

async def get_all_users(db: AsyncSession, token_data: dict):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if db_user.role != models.Role.ADMIN.value:
        raise HTTPException(status_code=400, detail="Only admin users can access this resource.")
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.is_deleted == False))
    return result.scalars().all()

async def get_authors(db: AsyncSession):
    result = await db.execute(select(models.Author))
    return result.scalars().all()

async def add_book(db: AsyncSession, token_data: dict, book: schemas.BookCreate):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role == models.Role.USER:
        raise HTTPException(status_code=400, detail="User does not have permission to add books.")
    if current_user.role == models.Role.AUTHOR:
        db_book = models.Book(title=book.title, category = book.category)
        db.add(db_book)
        await db.commit()
        await db.refresh(db_book)
        for author_id in book.authors_id:
            book_author = models.BookAuthor(book_id=db_book.id, author_id = author_id)
            db.add(book_author)
        await db.commit()
        return f"id: {db_book.id}"

async def remove_book(db: AsyncSession, token_data: dict, book_id: int):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role == models.Role.USER:
        raise HTTPException(status_code=400, detail="User does not have permission to remove books.")
    if current_user.role == models.Role.AUTHOR:
        result = await db.execute(select(models.Book).where(models.Book.id == book_id, models.Book.is_deleted == False))
        book = result.scalar_one_or_none()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found or you do not have permission to remove this book.")
        book.is_deleted = True
        await db.commit()
    elif current_user.role == models.Role.ADMIN:
        result = await db.execute(select(models.Book).where(models.Book.id == book_id, models.Book.delete_time.is_(None)))
        book = result.scalar_one_or_none()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        book.is_deleted = True
        await db.commit()

async def update_book(db: AsyncSession, token_data: dict, book_id: int, book_update: schemas.BookUpdate):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role == models.Role.USER:
        raise HTTPException(status_code=400, detail="User does not have permission to update books.")

    if current_user.role == models.Role.AUTHOR:
        result = await db.execute(select(models.Book).where(models.Book.id == book_id, models.Book.is_deleted == False))
        book = result.scalar_one_or_none()
        result = await db.execute(select(models.BookAuthor).where(models.BookAuthor.book_id == book_id, models.BookAuthor.author_id == current_user.id))
        book_author = result.scalar_one_or_none()
        if book_author is None or book is None:
            raise HTTPException(status_code=404, detail="Book not found or you do not have permission to update this book.")
        if book_update.title is not None:
            book.title = book_update.title
        if book_update.category is not None:
            book.category = book_update.category
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
        if book_update.category is not None:
            book.category = book_update.category
        await db.commit()
        await db.refresh(book)
        return book

async def search_books(db: AsyncSession,title: str | None = None,author: str | None = None,id: int | None = None,limit: int = 10, offset: int = 0):
    query = select(models.Book)

    if author:
        query = query.join(models.BookAuthor, models.BookAuthor.book_id == models.Book.id)\
                     .join(models.Author, models.Author.id == models.BookAuthor.author_id)\
                     .where(
                         models.Author.username.ilike(f"%{author}%"),
                         models.Author.is_deleted == False,
                         models.Book.is_deleted == False
                     )

    if title:
        query = query.where(
            models.Book.title.ilike(f"%{title}%"),
            models.Book.is_deleted == False
        )

    if id is not None:
        query = query.where(models.Book.id == id)

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()

async def add_edition(db: AsyncSession, token_data: dict, edition: schemas.EditionCreate):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role == models.Role.USER:
        raise HTTPException(status_code=400, detail="User does not have permission to add books.")
    if current_user.role == models.Role.AUTHOR:
        result = await db.execute(select(models.Book).where(models.Book.id == edition.book_id,models.Book.is_deleted == False))
        book = result.scalar_one_or_none()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        result = await db.execute(select(models.BookAuthor).where(models.BookAuthor.book_id == edition.book_id, models.BookAuthor.author_id == current_user.id))
        bookauthor = result.scalar_one_or_none()
        if bookauthor is None:
            raise HTTPException(status_code=400, detail= "you are not the author of this book")
        if edition.amount is not None and edition.amount < 0:
            raise HTTPException(status_code=400, detail="amount cannot be negative")

        if edition.price is not None and edition.price < 0:
            raise HTTPException(status_code=400, detail="price cannot be negative")
        new_edition = models.Edition(book_id=edition.book_id, price=edition.price, amount = edition.amount, language=edition.language, specefic_edition_title = edition.specefic_edition_title)
        db.add(new_edition)
        await db.commit()
        await db.refresh(new_edition)
        return new_edition

async def buy(db: AsyncSession, edition_ids: list[int], token_data: dict):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role != models.Role.USER:
        raise HTTPException(status_code=400, detail="Only users can buy books.")
    final_price = 0
    for edition_id in edition_ids:
        result = await db.execute(select(models.Edition).where(models.Edition.id == edition_id, models.Edition.is_deleted == False))
        edition = result.scalar_one_or_none()
        if edition is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        if edition.amount <= 0:
            raise HTTPException(status_code=400, detail="Book is out of stock.")
        final_price += edition.price
    if current_user.wallet_amount < final_price:
        raise HTTPException(status_code=400, detail="Insufficient funds in wallet.")
    current_user.wallet_amount -= final_price
    for edition_id in edition_ids:
        result = await db.execute(select(models.Edition).where(models.Edition.id == edition_id, models.Edition.is_deleted == False))
        edition = result.scalar_one_or_none()
        if edition is not None:
            edition.amount -= 1
    new_order = models.Order(user_id=current_user.id, state=models.OrderState.WAITING.value, final_price=final_price, date=str(datetime.utcnow()))
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    for edition_id in edition_ids:
        order_edition = models.OrderEdition(order_id=new_order.id, edition_id =edition_id)
        db.add(order_edition)
    await db.commit()
    return new_order

async def get_order(db: AsyncSession, token_data: dict):
    result = await db.execute(
        select(models.BaseUser).where(
            models.BaseUser.id == token_data["user_id"],
            models.BaseUser.is_deleted == False
        )
    )
    current_user = result.scalar_one_or_none()

    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role == models.Role.USER:
        result = await db.execute(
            select(models.Order).where(models.Order.user_id == current_user.id)
        )
        orders = result.scalars().all()

    elif current_user.role == models.Role.AUTHOR:
        result = await db.execute(
            select(models.BookAuthor.book_id).where(
                models.BookAuthor.author_id == current_user.id
            )
        )
        book_ids = result.scalars().all()

        result = await db.execute(
            select(models.Edition.id).where(models.Edition.book_id.in_(book_ids))
        )
        edition_ids = result.scalars().all()

        result = await db.execute(
            select(models.OrderEdition).where(
                models.OrderEdition.edition_id.in_(edition_ids)
            )
        )
        order_editions = result.scalars().all()

        result = await db.execute(
            select(models.Edition).where(models.Edition.id.in_(edition_ids))
        )
        editions = result.scalars().all()

        result = await db.execute(
            select(models.Order).where(
                models.Order.id.in_([oe.order_id for oe in order_editions])
            )
        )
        order_map: dict[int, models.Order] = {o.id: o for o in result.scalars().all()}

        output = []
        for oe in order_editions:
            edition = next(e for e in editions if e.id == oe.edition_id)
            order = order_map.get(oe.order_id)

            output.append({
                "order_id": order.id if order else None,
                "order_state": order.state if order else None,
                "date": order.date if order else None,
                "edition_id": edition.id,
                "price": edition.price,
            })

        return output

    elif current_user.role == models.Role.ADMIN:
        result = await db.execute(select(models.Order))
        orders = result.scalars().all()
        return orders

async def update_order_state(db: AsyncSession, token_data: dict, order_id: int, new_state: schemas.OrderState):
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if order.state == schemas.OrderState.CANCELED.value or order.state == schemas.OrderState.DONE.value:
        raise HTTPException(status_code=400, detail="Cannot update a completed or canceled order.")
    else:
        if current_user.role == models.Role.USER:
            if order.user_id != current_user.id:
                raise HTTPException(status_code=403, detail="You do not have permission to update this order.")
            if new_state == schemas.OrderState.CANCELED:
                order.state = new_state.value
                result = await db.execute(select(models.OrderEdition.edition_id).where(models.OrderEdition.order_id == order_id))
                edition_ids = result.scalars().all()
                result = await db.execute(select(models.Edition).where(models.Edition.id.in_(edition_ids)))
                editions = result.scalars().all()
                for edition in editions:
                    edition.amount += 1
                current_user.wallet_amount += order.final_price
                await db.commit()
                return order
            else:
                raise HTTPException(status_code=400, detail="Users can only cancel their orders.")

async def update_order_state_auto(db: AsyncSession, order_id: int):

    result = await db.execute(
        select(models.OrderEdition.state).where(
            models.OrderEdition.order_id == order_id
        )
    )
    states = result.scalars().all()

    if not states:
        return

    if all(s == models.OrderItemState.DONE.value for s in states):
        new_state = models.OrderState.DONE

    elif all(s == models.OrderItemState.REJECTED.value for s in states):
        new_state = models.OrderState.CANCELED

    elif any(s == models.OrderItemState.ACCEPTED.value for s in states):
        new_state = models.OrderState.IN_PROCCESE

    else:
        new_state = models.OrderState.WAITING

    result = await db.execute(
        select(models.Order).where(models.Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if order is None:
        return

    order.state = new_state.value # type: ignore[attr-defined]

    await db.commit()

async def update_order_edition_state(db: AsyncSession,token_data: dict,order_id: int,edition_id: int,new_state: schemas.OrderItemState):
    result = await db.execute(
        select(models.BaseUser).where(
            models.BaseUser.id == token_data["user_id"],
            models.BaseUser.is_deleted == False
        )
    )
    current_user = result.scalar_one_or_none()

    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role != models.Role.AUTHOR:
        raise HTTPException(status_code=403, detail="Only authors can update order items")

    result = await db.execute(
        select(models.BookAuthor.book_id).where(
            models.BookAuthor.author_id == current_user.id
        )
    )
    book_ids = result.scalars().all()

    result = await db.execute(
        select(models.Edition.id).where(models.Edition.book_id.in_(book_ids))
    )
    edition_ids = result.scalars().all()

    if edition_id not in edition_ids:
        raise HTTPException(status_code=403, detail="This edition does not belong to you")

    result = await db.execute(
        select(models.OrderEdition).where(
            models.OrderEdition.order_id == order_id,
            models.OrderEdition.edition_id == edition_id
        )
    )
    order_edition = result.scalar_one_or_none()

    if order_edition is None:
        raise HTTPException(status_code=404, detail="Order item not found")
    
    result = await db.execute(select(models.Order).where(models.Order.id == order_id))
    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.state == models.OrderState.CANCELED.value:
        raise HTTPException(
            status_code=400,
            detail="Cannot update items of a canceled order"
        )

    if order_edition.state in [models.OrderItemState.REJECTED.value,models.OrderItemState.DONE.value]:
        raise HTTPException(status_code=400,detail="This item is already rejected or done and cannot be updated.")

    order_edition.state = new_state.value

    await db.commit()
    await update_order_state_auto(db=db,order_id=order_edition.order_id)
    return order_edition

async def increase_wallet_amount(db: AsyncSession, token_data: dict, amount: int):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role != models.Role.USER:
        raise HTTPException(status_code=400, detail="Only users can increase wallet amount.")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero.")
    current_user.wallet_amount += amount
    transfer = models.Transaction(user_id=current_user.id, amount=amount, type=models.TransactionType.DEPOSIT, date=str(datetime.utcnow()))
    db.add(transfer)
    await db.commit()
    return current_user.wallet_amount

async def transfer_wallet_amount(db: AsyncSession, token_data: dict, recipient_email: str, amount: int):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    sender = result.scalar_one_or_none()
    if sender is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if sender.role != models.Role.USER:
        raise HTTPException(status_code=400, detail="Only users can transfer wallet amount.")
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.email == recipient_email, models.BaseUser.is_deleted == False))
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
    sender_transaction = models.Transaction(user_id=sender.id, amount=amount, type=models.TransactionType.SEND.value, date=str(datetime.utcnow()))
    recipient_transaction = models.Transaction(user_id=recipient.id, amount=amount, type=models.TransactionType.RECEIVE.value, date=str(datetime.utcnow()))
    db.add(sender_transaction)
    db.add(recipient_transaction)
    await db.commit()
    return {"sender_wallet_amount": sender.wallet_amount, "recipient_wallet_amount": recipient.wallet_amount}

async def deposit(token_data: dict, amount: int, db: AsyncSession):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
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
    transfer = models.Transaction(user_id=current_user.id, amount=amount, type=models.TransactionType.DEPOSIT.value, date=str(datetime.utcnow()))
    db.add(transfer)
    await db.commit()

async def confirm_deposit(token_data: dict, amount: int, db: AsyncSession):
    ...
    
async def withdraw_wallet_amount(db: AsyncSession, token_data: dict, amount: int):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
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
    transfer = models.Transaction(user_id=current_user.id, amount=amount, type=models.TransactionType.WITHDRAWAL.value, date=str(datetime.utcnow()))
    db.add(transfer)
    await db.commit()
    return current_user.wallet_amount

async def wallet_info(db: AsyncSession, token_data: dict):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    result = await db.execute(select(models.Transaction).where(models.Transaction.user_id == current_user.id))
    transactions = result.scalars().all()
    transactions_data = []
    for transaction in transactions:
        transactions_data.append({
            "amount": transaction.amount,
            "type": transaction.type,
            "date": transaction.date
        })
    return {"wallet_amount": current_user.wallet_amount, "transactions": transactions_data}

async def borrow_edition(db: AsyncSession,token_data: dict,edition_id: int):
    result = await db.execute(
        select(models.User)
                          .join(models.BaseUser,models.BaseUser.id == models.User.id)
                          .where(models.User.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.plan == models.UserPlan.BRONZE:
        raise HTTPException(status_code=403, detail="you are not allowed to borrow books")
    result = await db.execute(
        update(models.Edition)
        .where(models.Edition.id == edition_id, models.Edition.amount > 0)
        .values(amount=models.Edition.amount - 1)
        .returning(models.Edition.id)
    )
    edition = result.scalar_one_or_none()

    if edition is None:
        raise HTTPException(status_code=404, detail="Edition not found")

    limits = {models.UserPlan.SILVER: 1,models.UserPlan.GOLD: 5,models.UserPlan.PLATINUM: 10}
    result = await db.execute(select(func.count(models.Borrow.id)).where(models.Borrow.user_id == current_user.id, models.Borrow.status.in_([models.BorrowStatus.ACTIVE, models.BorrowStatus.OVERDUE])))
    count_of_borrows = result.scalar() or 0
    if count_of_borrows >= limits[current_user.plan]:
        raise HTTPException(status_code=403,detail="Borrow limit reached for your plan")

    loan_periods = {models.UserPlan.SILVER: 7,models.UserPlan.GOLD: 14,models.UserPlan.PLATINUM: 30}
    borrowed_at = datetime.utcnow()
    due_at = borrowed_at + timedelta(days=loan_periods[current_user.plan])
    borrow = models.Borrow(user_id = current_user.id, edition_id = edition_id, borrowed_at = borrowed_at, due_at = due_at)
    db.add(borrow)
    await db.commit()
    await db.refresh(borrow)

async def assign_from_waitlist(db: AsyncSession, edition_id: int):

    result = await db.execute(
        select(models.Waitlist)
        .join(models.User, models.Waitlist.user_id == models.User.id)
        .where(models.Waitlist.edition_id == edition_id)
        .order_by(
            case(
                (models.User.plan == models.UserPlan.PLATINUM, 3),
                (models.User.plan == models.UserPlan.GOLD, 2),
                (models.User.plan == models.UserPlan.SILVER, 1),
            ).desc(),
            models.Waitlist.created_at.asc()
        )
    )

    wait_item = result.scalars().first()

    if wait_item is None:
        return

    await db.delete(wait_item)

    loan_periods = {models.UserPlan.SILVER: 7,models.UserPlan.GOLD: 14,models.UserPlan.PLATINUM: 30}
    borrowed_at = datetime.utcnow()

    result = await db.execute(select(models.User).where(models.User.id == wait_item.user_id))
    inwait_user = result.scalar_one_or_none()
    if inwait_user is None:
        return

    due_at = borrowed_at + timedelta(days=loan_periods[inwait_user.plan])

    borrow = models.Borrow(
        user_id=inwait_user.id,
        edition_id=edition_id,
        borrowed_at=borrowed_at,
        due_at=due_at,
        status=models.BorrowStatus.ACTIVE
    )

    db.add(borrow)

    await db.execute(
        update(models.Edition)
        .where(models.Edition.id == edition_id, models.Edition.amount > 0)
        .values(amount=models.Edition.amount - 1)
    )

    return borrow

async def return_borrow(db: AsyncSession, token_data: dict, borrow_id: int):

    result = await db.execute(
        select(models.BaseUser).where(
            models.BaseUser.id == token_data["user_id"],
            models.BaseUser.is_deleted == False
        )
    )
    current_user = result.scalar_one_or_none()

    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    result = await db.execute(
        select(models.Borrow).where(models.Borrow.id == borrow_id)
    )
    borrow = result.scalar_one_or_none()

    if borrow is None:
        raise HTTPException(status_code=404, detail="Borrow not found")

    if borrow.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your borrow")

    if borrow.status == models.BorrowStatus.RETURNED:
        raise HTTPException(status_code=400, detail="Already returned")


    borrow.status = models.BorrowStatus.RETURNED
    borrow.returned_at = datetime.utcnow()

    inwait_borrow = await assign_from_waitlist(db=db, edition_id=borrow.edition_id)

    if not inwait_borrow:
        await db.execute(
            update(models.Edition)
            .where(models.Edition.id == borrow.edition_id)
            .values(amount=models.Edition.amount + 1)
        )

    await db.commit()
    await db.refresh(borrow)

    return borrow

async def get_on_returned_borrow(db: AsyncSession, token_data: dict):
    result = await db.execute(
        select(models.BaseUser).where(
            models.BaseUser.id == token_data["user_id"],
            models.BaseUser.is_deleted == False
        )
    )
    current_user = result.scalar_one_or_none()

    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role != models.Role.AUTHOR:
        raise HTTPException(status_code=403, detail="Only authors can view requests")

    result = await db.execute(
        select(models.Borrow)
        .join(models.Edition, models.Borrow.edition_id == models.Edition.id)
        .join(models.Book, models.Edition.book_id == models.Book.id)
        .join(models.BookAuthor, models.Book.id == models.BookAuthor.book_id)
        .where(
            models.BookAuthor.author_id == current_user.id,
            models.Borrow.status != models.BorrowStatus.RETURNED
        )
    )

    borrows = result.scalars().all()
    return borrows

async def add_to_waitlist(db: AsyncSession, token_data: dict, edition_id: int):

    result = await db.execute(
        select(models.BaseUser).where(
            models.BaseUser.id == token_data["user_id"],
            models.BaseUser.is_deleted == False
        )
    )
    current_user = result.scalar_one_or_none()

    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")

    if current_user.role != models.Role.USER:
        raise HTTPException(status_code=403, detail="Only users are allowed")

    result = await db.execute(
        select(models.Edition).where(models.Edition.id == edition_id)
    )
    edition = result.scalar_one_or_none()

    if edition is None:
        raise HTTPException(status_code=404, detail="Edition not found")

    result = await db.execute(
        select(models.Waitlist).where(
            models.Waitlist.user_id == current_user.id,
            models.Waitlist.edition_id == edition_id
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Already in waitlist")

    wait = models.Waitlist(
        user_id=current_user.id,
        edition_id=edition_id,
        created_at=datetime.utcnow()
    )

    db.add(wait)
    await db.commit()
    await db.refresh(wait)

    return wait

async def best_author_in_sell(db: AsyncSession):
    result = await db.execute(
    select(
        models.Author.id,
        models.BaseUser.username,
        func.count(models.OrderEdition.edition_id).label("total_sales")
    )
    .join(models.BaseUser, models.BaseUser.id == models.Author.id)
    .join(models.BookAuthor, models.BookAuthor.author_id == models.Author.id)
    .join(models.Book, models.Book.id == models.BookAuthor.book_id)
    .join(models.Edition, models.Edition.book_id == models.Book.id)
    .join(models.OrderEdition, models.OrderEdition.edition_id == models.Edition.id)
    .join(models.Order, models.Order.id == models.OrderEdition.order_id)
    .where(
        models.Order.state == models.OrderState.DONE,
        models.OrderEdition.state == models.OrderItemState.DONE
    )
    .group_by(models.Author.id, models.BaseUser.username)
    .order_by(desc("total_sales")).limit(20)
)
    return result.all()

async def best_author_in_income(db:AsyncSession):
    result = await db.execute(
        select(
            models.Author.id,
            models.BaseUser.username,
            func.sum(models.Edition.price).label("total_income"))
            .join(models.BaseUser,models.BaseUser.id == models.Author.id)
            .join(models.BookAuthor,models.BookAuthor.author_id == models.Author.id)
            .join(models.Book,models.Book.id == models.BookAuthor.book_id)
            .join(models.Edition,models.Edition.book_id == models.Book.id)
            .join(models.OrderEdition,models.OrderEdition.edition_id == models.Edition.id)
            .join(models.Order,models.Order.id == models.OrderEdition.order_id)
            .where(models.Order.state == models.OrderState.DONE,
                   models.OrderEdition.state == models.OrderItemState.DONE)
                   .group_by(models.Author.id, models.BaseUser.username)
                   .order_by(desc("total_income")).limit(20)
                   )
    return result.all()

async def best_edition_in_sell(db: AsyncSession):
    result = await db.execute(
        select(models.Book.id,
               models.Book.title,
               models.Edition.id,
               models.Edition.specefic_edition_title,
               func.count(models.OrderEdition.id).label("total_sales"))
               .join(models.Edition,models.Book.id == models.Edition.book_id)
               .join(models.OrderEdition,models.OrderEdition.edition_id == models.Edition.id)
               .join(models.Order,models.Order.id == models.OrderEdition.order_id)
               .where(models.Order.state == models.OrderState.DONE,
                      models.OrderEdition.state == models.OrderItemState.DONE)
                      .group_by(models.Edition.id, models.Book.id,models.Book.title,models.Edition.specefic_edition_title)
                      .order_by(desc("total_sales")).limit(20)
    )
    return result.all()

async def best_category_in_sell(db: AsyncSession):
    result = await db.execute(
        select(models.Book.category,
               func.count(models.Book.category).label("total_sales"))
               .join(models.Edition,models.Edition.book_id == models.Book.id)
               .join(models.OrderEdition,models.OrderEdition.edition_id == models.Edition.id)
               .join(models.Order,models.Order.id == models.OrderEdition.order_id)
               .where(models.OrderEdition.state == models.OrderItemState.DONE,
                      models.Order.state == models.OrderState.DONE)
                      .group_by(models.Book.category)
                      .order_by(desc("total_sales")).limit(20)
    )
    return result.all()

async def monthly_income(db:AsyncSession, token_data: dict):
    result = await db.execute(select(models.BaseUser).where(models.BaseUser.id == token_data["user_id"], models.BaseUser.is_deleted == False))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=400, detail="Invalid token user")
    if current_user.role != models.Role.AUTHOR:
        raise HTTPException(status_code=403, detail="Only authors have income")
    result = await db.execute(
        select(models.BaseUser.id,
               models.BaseUser.username,
               func.sum(models.Edition.price).label("monthly_income"))
               .join(models.BookAuthor,models.BookAuthor.author_id == models.BaseUser.id)
               .join(models.Edition, models.Edition.book_id == models.BookAuthor.book_id)
               .join(models.OrderEdition, models.OrderEdition.edition_id == models.Edition.id)
               .join(models.Order,models.Order.id == models.OrderEdition.order_id)
               .where(models.OrderEdition.state == models.OrderItemState.DONE,
                      models.Order.state == models.OrderState.DONE)
                      .group_by(models.BaseUser.id, models.BaseUser.username)
    )
    return result.scalar_one_or_none()

async def best_user_in_buy(db: AsyncSession):
    result = await db.execute(
        select(models.BaseUser.id,
               models.BaseUser.username,
               models.User.plan,
               func.count(models.OrderEdition).label("total_buys"))
               .join(models.User,models.User.id == models.BaseUser.id)
               .join(models.Order,models.Order.user_id == models.User.id)
               .join(models.OrderEdition, models.OrderEdition.order_id == models.Order.id)
               .where(models.Order.state == models.OrderState.DONE, models.OrderEdition.state == models.OrderItemState.DONE)
               .group_by(models.BaseUser.id, models.BaseUser.username, models.User.plan)
               .order_by(desc("total_buys")).limit(20)
    )
    return result.all()

async def best_edition_in_borrow(db: AsyncSession):
    result = await db.execute(
        select(models.Book.id,
               models.Book.title,
               models.Book.category,
               models.Edition.id,
               models.Edition.specefic_edition_title,
               func.count(models.Borrow.id).label("total_borrow"))
               .join(models.Edition, models.Edition.book_id == models.Book.id)
               .join(models.Borrow, models.Borrow.edition_id == models.Edition.id)
               .group_by(models.Edition.id,models.Book.id,models.Book.category,models.Book.title,models.Edition.specefic_edition_title)
               .order_by(desc("total_borrow"))
               .limit(20)
    )
    return result.all()

async def user_with_over_due(db: AsyncSession):
    result = await db.execute(
        select(models.BaseUser.id,
               models.BaseUser.username,
               models.Borrow.id,
               models.Borrow.borrowed_at,
               models.Borrow.due_at)
               .join(models.Borrow,models.Borrow.user_id == models.BaseUser.id)
               .where(models.Borrow.status == models.BorrowStatus.OVERDUE)
    )
    return result.all()

async def mark_overdue_borrows(db: AsyncSession):
    await db.execute(
        update(models.Borrow)
        .where(
            and_(
                models.Borrow.status == models.BorrowStatus.ACTIVE,
                models.Borrow.due_at < datetime.now(timezone.utc)
            )
        )
        .values(status=models.BorrowStatus.OVERDUE)
    )

    await db.commit()