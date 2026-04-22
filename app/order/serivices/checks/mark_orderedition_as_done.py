from app.unit_of_work import UnitOfWork
from app.order.models import enums
from datetime import datetime, timedelta

async def mark_orderedition_as_done(uow: UnitOfWork):
    now = datetime.utcnow()
    date = now - timedelta(days=5)
    async with uow:
        order_editions = await uow.orderedition.get_by_last_modify_and_state(state=enums.OrderItemState.PREPARING,date=date)
        for order_editioin in order_editions:
            await uow.orderedition.update_state(orderedition=order_editioin,new_state=enums.OrderItemState.DONE)
            edition  = await uow.edition.get_by_id(order_editioin.edition_id)
            authors = await uow.bookauthor.get_by_book_id(book_id=edition.book_id)
            count_of_author = await uow.bookauthor.count_of_author(book_id=edition.book_id)
            take = order_editioin.price / count_of_author
            for author in authors:
                await uow.baseusers.increase_wallet_amount(user=author,change=take)
