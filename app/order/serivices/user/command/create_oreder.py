from app.unit_of_work import UnitOfWork
from app.user.models.enums import Role
from app.order.models import model
from datetime import datetime

from app.exceptions.models.user import (
    InvalidTokenUser,
    OnlyUserHavePrimition
)

from app.exceptions.models.edition import (
    EditionNotFound,
    EditionOutOfStock
)

from app.exceptions.models.transaction import InsufficientFunds
from app.order.schemas.outputs import OrderResponse


async def create_order(
    uow: UnitOfWork,
    edition_ids: list[int],
    token_data: dict
):
    async with uow:

        current_user = await uow.baseusers.get_by_id(
            user_id=token_data["user_id"]
        )

        if current_user is None:
            raise InvalidTokenUser

        if current_user.role != Role.USER:
            raise OnlyUserHavePrimition

        editions = await uow.edition.get_by_ids(edition_ids)

        edition_map = {e.id: e for e in editions}

        missing = set(edition_ids) - set(edition_map.keys())

        if missing:
            raise EditionNotFound

        final_price = 0

        for edition in editions:

            if edition.amount <= 0:
                raise EditionOutOfStock

            final_price += edition.price

            edition.amount -= 1

        if current_user.wallet_amount < final_price:
            raise InsufficientFunds

        await uow.baseusers.decrease_wallet_amount(
            user=current_user,
            change=final_price
        )

        now = datetime.utcnow()

        new_order = model.Order(
            user_id=current_user.id,
            final_price=final_price,
            date=now
        )

        await uow.order.create_order(new_order)

        await uow.flush()

        order_editions = [
            model.OrderEdition(
                order_id=new_order.id,
                edition_id=edition.id,
                last_modify=now,
                price=edition.price
            )
            for edition in editions
        ]

        await uow.orderedition.create_many(order_editions)

        return OrderResponse.model_validate(new_order)