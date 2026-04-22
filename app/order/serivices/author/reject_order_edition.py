from fastapi import HTTPException
from app.unit_of_work import UnitOfWork
from app.user.models.enums import Role
from app.order.models import model, enums



async def rejec_order_edition(uow:UnitOfWork,order_edition_id: int, token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise HTTPException(status_code=400, detail="Invalid token user")
        if current_user.role == Role.USER:
            raise HTTPException(status_code=400, detail="User does not have permission to this.")
        order_edition = await uow.orderedition.get_by_order_edition_id(order_edition_id)
        if order_edition is None:
            raise HTTPException(status_code=400, detail="orderedition not found.")
        if current_user.role == Role.AUTHOR:
            edition = await uow.edition.get_by_id(order_edition.edition_id)
            book_author = await uow.bookauthor.get_by_authorid_and_bookid(author_id=current_user.id,book_id=edition.book_id)
            if book_author is None:
                raise HTTPException(status_code=400, detail="this is not your order edition.")
            await uow.orderedition.update_state(new_state=enums.OrderItemState.CANCELED,orderedition=order_edition)
        return order_edition