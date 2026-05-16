from app.unit_of_work import UnitOfWork
from app.order.models import enums
from datetime import datetime, timedelta


async def mark_orderedition_as_done(uow: UnitOfWork):
    now = datetime.utcnow()
    date = now - timedelta(days=5)

    async with uow:
        order_editions = await uow.orderedition.get_by_last_modify_and_state(
            state=enums.OrderItemState.PREPARING,
            date=date
        )

        if not order_editions:
            return

        # batch ids
        edition_ids = list({oe.edition_id for oe in order_editions})

        editions = await uow.edition.get_by_ids(edition_ids)
        edition_map = {e.id: e for e in editions}

        book_ids = [e.book_id for e in editions]

        book_authors = await uow.bookauthor.get_by_book_ids(book_ids)

        grouped_authors: dict = {}
        for ba in book_authors:
            grouped_authors.setdefault(ba.book_id, []).append(ba)

        # update order editions batch
        order_edition_ids = [oe.order_edition_id for oe in order_editions]

        await uow.orderedition.many_update_state(
            order_edition_ids=order_edition_ids,
            new_state=enums.OrderItemState.DONE
        )

        # wallet calculation
        wallet_updates = []

        for oe in order_editions:
            edition = edition_map[oe.edition_id]
            authors = grouped_authors.get(edition.book_id, [])

            if not authors:
                continue

            take = oe.price / len(authors)

            for author in authors:
                wallet_updates.append((author.author_id, take))

        await uow.baseusers.many_increase_wallet(
            wallet_updates=wallet_updates
        )