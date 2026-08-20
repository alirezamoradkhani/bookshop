import unittest
from datetime import datetime, timezone
from types import SimpleNamespace

from app.borrow.models.enums import BorrowStatus
from app.borrow.services.borrow.borrow_edition import borrow_edition
from app.core.security import create_access_token, decode_token
from app.exceptions.models.borrow import ActiveBorrowExists
from app.exceptions.models.edition import InvalidAmount
from app.exceptions.models.order import DuplicateOrderEdition
from app.exceptions.models.transaction import InsufficientFunds
from app.order.models.enums import OrderState
from app.order.serivices.user.command.create_oreder import create_order
from app.search.service.normalize_query import normalize_query
from app.search.service.paginate import paginate
from app.transaction.services.command.deposit import deposit
from app.transaction.services.command.transfer import transfer
from app.transaction.services.command.withdraw import withdraw
from app.user.models.enums import Role, UserPlan


class FakeUnitOfWork:
    def __init__(self, **repositories):
        for name, repository in repositories.items():
            setattr(self, name, repository)
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, _traceback):
        if exc_type:
            self.rolled_back = True
        else:
            self.committed = True

    async def flush(self):
        return None


class FakeBaseUsers:
    def __init__(self, users):
        self.users = {user.id: user for user in users}

    async def get_by_id(self, user_id, **_kwargs):
        return self.users.get(user_id)

    async def get_by_ids(self, user_ids, **_kwargs):
        return [self.users[user_id] for user_id in user_ids if user_id in self.users]

    async def increase_wallet_amount(self, user, change):
        user.wallet_amount += change

    async def decrease_wallet_amount(self, user, change):
        user.wallet_amount -= change


class FakeTransactions:
    def __init__(self):
        self.items = []

    async def create(self, transaction):
        self.items.append(transaction)


class FakeEditions:
    def __init__(self, editions):
        self.editions = {edition.id: edition for edition in editions}
        self.updated = []

    async def get_by_ids(self, edition_ids, **_kwargs):
        return [self.editions[edition_id] for edition_id in edition_ids if edition_id in self.editions]

    async def get_by_id(self, edition_id, **_kwargs):
        return self.editions.get(edition_id)

    async def update_amount(self, edition, new_amount):
        edition.amount = new_amount
        self.updated.append((edition.id, new_amount))


class FakeOrders:
    def __init__(self):
        self.order = None

    async def create_order(self, order):
        order.id = 100
        order.state = OrderState.WAITING
        self.order = order


class FakeOrderEditions:
    def __init__(self):
        self.items = []

    async def create_many(self, items):
        self.items.extend(items)


class FakeOutbox:
    def __init__(self):
        self.events = []

    async def add(self, event):
        self.events.append(event)


class FakeBorrows:
    def __init__(self, active=None):
        self.active = active
        self.borrow = None

    async def get_active_by_user_and_edition(self, _user_id, _edition_id):
        return self.active

    async def create(self, new_borrow):
        new_borrow.id = 200
        new_borrow.status = BorrowStatus.ACTIVE
        new_borrow.is_overdue = False
        self.borrow = new_borrow


class CoreFlowTests(unittest.IsolatedAsyncioTestCase):
    def make_user(self, user_id=1, wallet_amount=100, role=Role.USER):
        return SimpleNamespace(
            id=user_id,
            username=f"user-{user_id}",
            email=f"user-{user_id}@example.com",
            role=role,
            wallet_amount=wallet_amount,
            plan_expire=None,
        )

    def test_access_token_round_trip_and_invalid_token(self):
        token = create_access_token({"user_id": 42, "role": Role.USER.value})

        payload = decode_token(token)

        self.assertEqual(payload["user_id"], 42)
        self.assertEqual(payload["role"], Role.USER.value)
        self.assertIn("exp", payload)
        self.assertIsNone(decode_token("not-a-token"))

    def test_query_normalization_and_pagination(self):
        self.assertEqual(normalize_query("  Dune  "), "dune")
        self.assertEqual(normalize_query(None), "")
        self.assertEqual(paginate([1, 2, 3, 4], page=2, size=2), [3, 4])

    async def test_deposit_and_transfer_update_wallets_and_record_transactions(self):
        sender = self.make_user(wallet_amount=100)
        receiver = self.make_user(user_id=2, wallet_amount=10)
        transactions = FakeTransactions()
        uow = FakeUnitOfWork(
            baseusers=FakeBaseUsers([sender, receiver]),
            transaction=transactions,
        )

        deposited = await deposit(uow, amount=25, token_data={"user_id": sender.id})
        transferred = await transfer(
            uow,
            amount=40,
            token_data={"user_id": sender.id},
            reciver_id=receiver.id,
        )

        self.assertEqual(deposited["wallet_amount"], 125)
        self.assertEqual(transferred["wallet_amount"], 85)
        self.assertEqual(receiver.wallet_amount, 50)
        self.assertEqual(len(transactions.items), 3)
        self.assertTrue(uow.committed)

    async def test_withdraw_rejects_insufficient_funds_without_mutation(self):
        user = self.make_user(wallet_amount=10)
        transactions = FakeTransactions()
        uow = FakeUnitOfWork(
            baseusers=FakeBaseUsers([user]),
            transaction=transactions,
        )

        with self.assertRaises(InsufficientFunds):
            await withdraw(uow, amount=11, token_data={"user_id": user.id})

        self.assertEqual(user.wallet_amount, 10)
        self.assertEqual(transactions.items, [])
        self.assertTrue(uow.rolled_back)

    async def test_deposit_rejects_non_positive_amount(self):
        user = self.make_user()
        uow = FakeUnitOfWork(baseusers=FakeBaseUsers([user]), transaction=FakeTransactions())

        with self.assertRaises(InvalidAmount):
            await deposit(uow, amount=0, token_data={"user_id": user.id})

    async def test_create_order_rejects_duplicate_editions(self):
        uow = FakeUnitOfWork()

        with self.assertRaises(DuplicateOrderEdition):
            await create_order(uow, edition_ids=[7, 7], token_data={"user_id": 1})

    async def test_create_order_debits_wallet_decrements_inventory_and_emits_event(self):
        user = self.make_user(wallet_amount=100)
        edition = SimpleNamespace(id=7, amount=2, price=40)
        editions = FakeEditions([edition])
        orders = FakeOrders()
        ordereditions = FakeOrderEditions()
        outbox = FakeOutbox()
        uow = FakeUnitOfWork(
            baseusers=FakeBaseUsers([user]),
            edition=editions,
            order=orders,
            orderedition=ordereditions,
            outbox=outbox,
        )

        result = await create_order(uow, edition_ids=[edition.id], token_data={"user_id": user.id})

        self.assertEqual(result.id, 100)
        self.assertEqual(result.final_price, 40)
        self.assertEqual(user.wallet_amount, 60)
        self.assertEqual(edition.amount, 1)
        self.assertEqual(len(ordereditions.items), 1)
        self.assertEqual(len(outbox.events), 1)

    async def test_borrow_rejects_duplicate_active_borrow(self):
        user = self.make_user()
        edition = SimpleNamespace(id=8, amount=1)
        uow = FakeUnitOfWork(
            baseusers=FakeBaseUsers([user]),
            edition=FakeEditions([edition]),
            user=SimpleNamespace(get_plan_by_id=lambda _user_id: UserPlan.GOLD),
            borrow=FakeBorrows(active=SimpleNamespace(id=99)),
            outbox=FakeOutbox(),
        )

        async def get_plan(_user_id):
            return UserPlan.GOLD

        uow.user.get_plan_by_id = get_plan

        with self.assertRaises(ActiveBorrowExists):
            await borrow_edition(uow, token_data={"user_id": user.id}, edition_id=edition.id)

    async def test_borrow_decrements_inventory_and_emits_event(self):
        user = self.make_user()
        edition = SimpleNamespace(id=8, amount=1)
        editions = FakeEditions([edition])
        borrows = FakeBorrows()
        outbox = FakeOutbox()

        async def get_plan(_user_id):
            return UserPlan.GOLD

        uow = FakeUnitOfWork(
            baseusers=FakeBaseUsers([user]),
            edition=editions,
            user=SimpleNamespace(get_plan_by_id=get_plan),
            borrow=borrows,
            outbox=outbox,
        )

        result = await borrow_edition(uow, token_data={"user_id": user.id}, edition_id=edition.id)

        self.assertEqual(result.id, 200)
        self.assertEqual(result.user_id, user.id)
        self.assertEqual(result.edition_id, edition.id)
        self.assertEqual(edition.amount, 0)
        self.assertEqual(len(outbox.events), 1)
        self.assertGreater(result.due_at, datetime.now(timezone.utc).replace(tzinfo=None))


if __name__ == "__main__":
    unittest.main()
