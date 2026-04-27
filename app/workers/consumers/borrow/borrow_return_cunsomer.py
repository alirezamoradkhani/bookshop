from datetime import datetime, timedelta
from app.user.models.enums import UserPlan
from app.borrow.models.model import Borrow,Waitlist
from app.unit_of_work import UnitOfWork

class BorrowReturnedConsumer:

    async def get_qualified_waitlist(self, uow:UnitOfWork, edition_id):

        waitlist = await uow.waitlist.get_by_edition_id_and_user_plan(
            edition_id=edition_id,
            user_plan=UserPlan.PLATINUM
        )
        if waitlist:
            return waitlist

        waitlist = await uow.waitlist.get_by_edition_id_and_user_plan(
            edition_id=edition_id,
            user_plan=UserPlan.GOLD
        )
        if waitlist:
            return waitlist

        return await uow.waitlist.get_by_edition_id_and_user_plan(
            edition_id=edition_id,
            user_plan=UserPlan.SILVER
        )

    async def give_book(self, uow:UnitOfWork, waitlist:Waitlist):

        now = datetime.utcnow()

        plan = await uow.user.get_plan_by_id(waitlist.user_id)

        if plan == UserPlan.BRONZE:
            return

        if plan == UserPlan.SILVER:
            days = 7
        elif plan == UserPlan.GOLD:
            days = 14
        else:
            days = 30

        due_at = now + timedelta(days=days)

        borrow = Borrow(
            user_id=waitlist.user_id,
            edition_id=waitlist.edition_id,
            borrowed_at=now,
            due_at=due_at
        )

        await uow.borrow.create(new_borrow=borrow)

        await uow.waitlist.delete(waitlist)


    async def handle(self, event: dict, uow:UnitOfWork):

        async with uow:

            edition_id = event["edition_id"]

            waitlist = await self.get_qualified_waitlist(uow, edition_id)

            if not waitlist:
                return

            await self.give_book(uow, waitlist)