from app.unit_of_work import UnitOfWork
from app.user.models.enums import Role
from app.order.models import model
from datetime import datetime
from app.exceptions.models.user import InvalidTokenUser,OnlyUserHavePrimition
from app.exceptions.models.edition import EditionNotFound,EditionOutOfStock
from app.exceptions.models.transaction import InsufficientFunds

async def create_order(uow:UnitOfWork,edition_ids: list[int], token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        
        if current_user.role != Role.USER:
            raise OnlyUserHavePrimition
        
        final_price = 0
        for edition_id in edition_ids:
            edition = await uow.edition.get_by_id(edition_id)
            if edition is None:
                raise EditionNotFound
            if edition.amount <= 0:
                raise EditionOutOfStock
            final_price += edition.price
            edition.amount -= 1
        if current_user.wallet_amount < final_price:
            raise InsufficientFunds
        await uow.baseusers.decrease_wallet_amount(user=current_user,change=final_price)
        new_order = model.Order(
            user_id = current_user.id
            ,final_price = final_price
            ,date = datetime.utcnow())
        await uow.order.create_order(new_order)
        await uow.flush()
        for edition_id in edition_ids:
            edition = await uow.edition.get_by_id(edition_id)
            new_orderedition = model.OrderEdition(
                order_id=new_order.id
                ,edition_id=edition.id
                ,last_modify=new_order.date
                ,price=edition.price
                )
            await uow.orderedition.create(new_orderedition)
            await uow.flush()
        return new_order