from app.unit_of_work import UnitOfWork
from app.user.models.enums import Role
from app.order.models import enums
from app.exceptions.models.user import InvalidTokenUser,OnlyAuthorPrimition,UserPermissionDenied
from app.exceptions.models.order_edition import OrderEditionNotFound,InvalidChangeStatus



async def accept_order_edition(uow:UnitOfWork,order_edition_id: int, token_data: dict):
    async with uow:
        current_user = await uow.baseusers.get_by_id(user_id= token_data["user_id"])
        if current_user is None:
            raise InvalidTokenUser
        if current_user.role == Role.USER:
            raise OnlyAuthorPrimition
        order_edition = await uow.orderedition.get_by_order_edition_id(order_edition_id)
        if order_edition is None:
            raise OrderEditionNotFound
        if order_edition.state != enums.OrderItemState.WAITING:
            raise InvalidChangeStatus
        if current_user.role == Role.AUTHOR:
            edition = await uow.edition.get_by_id(order_edition.edition_id)
            book_author = await uow.bookauthor.get_by_authorid_and_bookid(author_id=current_user.id,book_id=edition.book_id)
            if book_author is None:
                raise UserPermissionDenied
            await uow.orderedition.update_state(new_state=enums.OrderItemState.ACCEPTED,orderedition=order_edition)
        return order_edition