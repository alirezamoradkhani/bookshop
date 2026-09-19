from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from pymongo import ReturnDocument

from app.borrow.models.enums import BorrowStatus
from app.borrow.models.model import Borrow, Waitlist
from app.book.models.model import Book, BookAuthor, BookCategory
from app.edition.models.model import Edition, EditionLanguage
from app.mongo.database import MongoContext
from app.mongo.serialization import serialize
from app.order.models.enums import OrderItemState, OrderState
from app.order.models.model import Order, OrderEdition
from app.outbox.model import OutboxEvent
from app.transaction.models.model import Transaction
from app.user.models.enums import Role, UserPlan
from app.user.models.model import Admin, Author, BaseUser, User


class MongoRepository:
    collection: str
    model: type
    enum_fields: dict[str, type[Enum]] = {}

    def __init__(self, db: MongoContext):
        self.db = db

    async def _next_id(self) -> int:
        result = await self.db.collection("counters").find_one_and_update(
            {"_id": self.collection},
            {"$inc": {"value": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
            **self.db.options(),
        )
        return int(result["value"])

    def _make(self, data: dict[str, Any] | None):
        if data is None:
            return None
        payload = dict(data)
        payload.pop("_id", None)
        for field, enum_type in self.enum_fields.items():
            value = payload.get(field)
            if value is not None and not isinstance(value, enum_type):
                payload[field] = enum_type(value)
        return self.db.track(self.model(**payload), self.collection)

    async def _insert(self, obj: Any):
        object_id = getattr(obj, "id", None)
        if object_id is None:
            object_id = await self._next_id()
            if hasattr(obj, "order_edition_id"):
                obj.order_edition_id = object_id
            else:
                obj.id = object_id
        document = {"_id": object_id, **serialize(obj)}
        await self.db.collection(self.collection).insert_one(document, **self.db.options())
        self.db.track(obj, self.collection)
        return obj

    async def _find_one(self, query: dict[str, Any]):
        document = await self.db.collection(self.collection).find_one(query, **self.db.options())
        return self._make(document)

    async def _find(self, query: dict[str, Any] | None = None, sort: tuple[str, int] | None = None):
        cursor = self.db.collection(self.collection).find(query or {}, **self.db.options())
        if sort:
            cursor = cursor.sort(*sort)
        return [self._make(document) async for document in cursor]

    async def _replace(self, obj: Any):
        await self.db.collection(self.collection).replace_one(
            {"_id": obj.id}, {"_id": obj.id, **serialize(obj)}, upsert=True, **self.db.options()
        )

    async def _delete(self, obj: Any):
        await self.db.collection(self.collection).delete_one({"_id": obj.id}, **self.db.options())


class BaseUserRepository(MongoRepository):
    collection, model = "users", BaseUser

    def _make(self, data):
        if data is None:
            return None
        payload = dict(data)
        payload.pop("_id", None)
        role = payload.get("role", Role.USER.value)
        role = role if isinstance(role, Role) else Role(role)
        payload["role"] = role
        cls = {Role.USER: User, Role.AUTHOR: Author, Role.ADMIN: Admin}.get(role, BaseUser)
        if cls is User:
            plan = payload.get("plan", UserPlan.BRONZE)
            payload["plan"] = plan if isinstance(plan, UserPlan) else UserPlan(plan)
        return self.db.track(cls(**payload), self.collection)

    async def get_by_id(self, user_id: int, for_update: bool = False):
        return await self._find_one({"_id": user_id, "is_deleted": False})

    async def get_by_ids(self, user_ids: list[int], for_update: bool = False):
        return await self._find({"_id": {"$in": user_ids}, "is_deleted": False})

    async def get_by_username(self, user_name: str):
        return await self._find_one({"username": user_name, "is_deleted": False})

    async def get_by_email(self, user_email: str):
        return await self._find_one({"email": user_email, "is_deleted": False})

    async def create(self, new_user: BaseUser):
        return await self._insert(new_user)

    async def soft_delete(self, user: BaseUser):
        user.is_deleted = True
        return user

    async def update_wallet_amount(self, user: BaseUser, new_amount: int):
        user.wallet_amount = new_amount

    async def increase_wallet_amount(self, user: BaseUser, change: int):
        user.wallet_amount += change

    async def many_increase_wallet(self, wallet_updates: list[tuple[int, int]]):
        for user_id, change in wallet_updates:
            await self.db.collection(self.collection).update_one(
                {"_id": user_id}, {"$inc": {"wallet_amount": change}}, **self.db.options()
            )

    async def decrease_wallet_amount(self, user: BaseUser, change: int):
        user.wallet_amount -= change


class UserRepository(BaseUserRepository):
    async def create(self, id: int):
        return await self._insert(User(id=id))

    async def get_by_id(self, id: int):
        user = await super().get_by_id(id)
        return user if isinstance(user, User) else None

    async def update_plan(self, new_plan: UserPlan, id: int, ex: datetime):
        user = await self.get_by_id(id)
        if user is not None:
            user.plan, user.plan_expire = new_plan, ex
        return user

    async def change_user_plan(self, user: User, new_plan: UserPlan):
        user.plan = new_plan
        return user

    async def many_update_plan(self, user_ids: list[int], new_plan: UserPlan):
        await self.db.collection(self.collection).update_many(
            {"_id": {"$in": user_ids}}, {"$set": {"plan": serialize(new_plan)}}, **self.db.options()
        )

    async def get_plan_by_id(self, user_id: int):
        user = await self.get_by_id(user_id)
        return user.plan if user else None

    async def get_plan_by_exp_date(self, now: datetime):
        return await self._find({"plan_expire": {"$lt": now}, "plan": {"$ne": UserPlan.BRONZE.value}})


class AuthorRepository(BaseUserRepository):
    async def create(self, id: int):
        return await self._insert(Author(id=id))

    async def get_by_id(self, id: int):
        user = await super().get_by_id(id)
        return user if isinstance(user, Author) else None

    async def get_by_name(self, name: str):
        user = await self._find_one({"username": name, "role": Role.AUTHOR.value})
        return user

    async def get_by_names(self, names: list[str]):
        return await self._find({"username": {"$in": names}, "role": Role.AUTHOR.value})

    async def get_by_ids(self, ids: list[int]):
        return await self._find({"_id": {"$in": ids}, "role": Role.AUTHOR.value})

    async def search(self, id=None, name=None):
        query: dict[str, Any] = {"role": Role.AUTHOR.value}
        if id:
            query["_id"] = id
        if name:
            query["username"] = {"$regex": name, "$options": "i"}
        return await self._find(query)


class AdminRepository(BaseUserRepository):
    async def create(self, id: int):
        return await self._insert(Admin(id=id))


class BookRepository(MongoRepository):
    collection, model = "books", Book

    async def create_book(self, new_book: Book):
        return await self._insert(new_book)

    async def get_by_id(self, id: int):
        return await self._find_one({"_id": id, "is_deleted": False})

    async def get_by_external_id(self, external_provider: str, external_id: str):
        return await self._find_one({"external_provider": external_provider, "external_id": external_id})

    async def update_book_title(self, book: Book, title: str):
        book.title = title

    async def delete_book(self, book: Book):
        book.is_deleted = True

    async def search_books(self, title=None, category=None, author_id=None):
        query: dict[str, Any] = {"is_deleted": False}
        if title:
            query["title"] = {"$regex": title, "$options": "i"}
        if category:
            query["categories"] = category
        if author_id:
            query["author_ids"] = author_id
        return await self._find(query)

    async def get_all(self):
        return await self._find({"is_deleted": False})


class BookAuthorRepository(MongoRepository):
    collection, model = "book_authors", BookAuthor

    async def create(self, book_author: BookAuthor):
        return await self._insert(book_author)

    async def create_many(self, items: list[BookAuthor]):
        for item in items:
            await self._insert(item)
            await self.db.collection("books").update_one(
                {"_id": item.book_id}, {"$addToSet": {"author_ids": item.author_id}}, **self.db.options()
            )

    async def get_by_authorid_and_bookid(self, book_id: int, author_id: int):
        return await self._find_one({"book_id": book_id, "author_id": author_id})

    async def get_by_author_id(self, author_id):
        return await self._find({"author_id": author_id})

    async def get_by_book_id(self, book_id: int):
        return await self._find({"book_id": book_id})

    async def get_by_book_ids(self, book_ids: list[int]):
        return await self._find({"book_id": {"$in": book_ids}})

    async def count_of_author(self, book_id: int):
        return len(await self.get_by_book_id(book_id))


class BookCategoryRepository(MongoRepository):
    collection, model = "book_categories", BookCategory

    async def create(self, book_category: BookCategory):
        return await self._insert(book_category)

    async def create_many(self, items: list[BookCategory]):
        for item in items:
            await self._insert(item)
            await self.db.collection("books").update_one(
                {"_id": item.book_id}, {"$addToSet": {"categories": item.category}}, **self.db.options()
            )

    async def delete(self, book_category: BookCategory):
        await self._delete(book_category)
        await self.db.collection("books").update_one(
            {"_id": book_category.book_id}, {"$pull": {"categories": book_category.category}}, **self.db.options()
        )

    async def get_by_book_id(self, book_id: int):
        return await self._find({"book_id": book_id})

    async def delete_by_book_id(self, book_id: int):
        await self.db.collection(self.collection).delete_many({"book_id": book_id}, **self.db.options())
        await self.db.collection("books").update_one({"_id": book_id}, {"$set": {"categories": []}}, **self.db.options())


class EditionRepository(MongoRepository):
    collection, model = "editions", Edition

    async def create_edition(self, new_edition: Edition):
        return await self._insert(new_edition)

    async def get_by_id(self, edition_id: int, for_update: bool = False):
        return await self._find_one({"_id": edition_id, "is_deleted": False})

    async def get_by_ids(self, edition_ids: list[int], for_update: bool = False):
        return await self._find({"_id": {"$in": edition_ids}, "is_deleted": False})

    async def update_amount(self, edition: Edition, new_amount: int):
        edition.amount = new_amount

    async def update_price(self, edition: Edition, new_price: int):
        edition.price = new_price

    async def soft_delete(self, edition: Edition):
        edition.is_deleted = True

    async def get_by_book_id(self, book_id: int):
        return await self._find({"book_id": book_id})

    async def get_by_book_ids(self, book_ids: list[int]):
        return await self._find({"book_id": {"$in": book_ids}})


class EditionLanguageRepository(MongoRepository):
    collection, model = "edition_languages", EditionLanguage

    async def create(self, edition_language: EditionLanguage):
        return await self._insert(edition_language)

    async def create_many(self, items: list[EditionLanguage]):
        for item in items:
            await self._insert(item)


class OrderRepository(MongoRepository):
    collection, model = "orders", Order
    enum_fields = {"state": OrderState}

    async def create_order(self, order: Order):
        return await self._insert(order)

    async def get_by_id(self, order_id: int):
        return await self._find_one({"_id": order_id})

    async def update_order_state(self, order: Order, new_state: OrderState):
        order.state = new_state

    async def update_final_price(self, order: Order, change: int):
        order.final_price -= change

    async def many_update_state(self, order_ids: list[int], new_state):
        await self.db.collection(self.collection).update_many(
            {"_id": {"$in": order_ids}}, {"$set": {"state": serialize(new_state)}}, **self.db.options()
        )

    async def get_by_state(self, state: OrderState):
        return await self._find({"state": serialize(state)})

    async def get_by_user_id(self, id: int):
        return await self._find({"user_id": id})


class OrderEditionRepository(MongoRepository):
    collection, model = "order_editions", OrderEdition
    enum_fields = {"state": OrderItemState}

    async def create(self, orderedition: OrderEdition):
        return await self._insert(orderedition)

    async def create_many(self, order_editions: list[OrderEdition]):
        for item in order_editions:
            await self._insert(item)

    async def update_state(self, new_state: OrderItemState, orderedition: OrderEdition):
        orderedition.state = new_state
        orderedition.last_modify = datetime.utcnow()

    async def many_update_state(self, order_edition_ids: list[int], new_state: OrderItemState):
        await self.db.collection(self.collection).update_many(
            {"_id": {"$in": order_edition_ids}},
            {"$set": {"state": serialize(new_state), "last_modify": datetime.utcnow()}},
            **self.db.options(),
        )

    async def get_by_order_id(self, order_id: int):
        return await self._find({"order_id": order_id})

    async def get_by_order_edition_id(self, order_edition_id: int):
        return await self._find_one({"_id": order_edition_id})

    async def get_by_state(self, state: OrderItemState):
        return await self._find({"state": serialize(state)})

    async def get_by_last_modify(self, date: datetime):
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        return await self._find({"last_modify": {"$gte": start, "$lt": start + timedelta(days=1)}})

    async def get_by_last_modify_and_state(self, date: datetime, state: OrderItemState):
        return await self._find({"last_modify": {"$lt": date}, "state": serialize(state)})

    async def get_orderedition_by_list_of_edition(self, editions: list[Edition]):
        return await self._find({"edition_id": {"$in": [edition.id for edition in editions]}})

    async def get_by_order_ids(self, order_ids: list[int]):
        return await self._find({"order_id": {"$in": order_ids}})


class Borrowpository(MongoRepository):
    collection, model = "borrows", Borrow
    enum_fields = {"status": BorrowStatus}

    async def create(self, new_borrow: Borrow):
        return await self._insert(new_borrow)

    async def get_by_id(self, borrow_id: int, for_update: bool = False):
        return await self._find_one({"_id": borrow_id})

    async def get_by_user_id(self, user_id: int):
        return await self._find({"user_id": user_id}, ("borrowed_at", -1))

    async def get_active_by_user_and_edition(self, user_id: int, edition_id: int):
        return await self._find_one({"user_id": user_id, "edition_id": edition_id, "status": BorrowStatus.ACTIVE.value})

    async def update_status(self, borrow: Borrow, new_status: BorrowStatus):
        borrow.status = new_status

    async def set_Return_time(self, borrow: Borrow, return_time: datetime):
        borrow.returned_at = return_time

    async def get_owerdue_by_date(self, now: datetime):
        return await self._find({"due_at": {"$lt": now}, "status": BorrowStatus.ACTIVE.value, "is_overdue": False})

    async def mark_as_owerdue(self, borrow: Borrow):
        borrow.is_overdue = True

    async def mark_many_as_overdue(self, borrows: list[Borrow]):
        await self.db.collection(self.collection).update_many(
            {"_id": {"$in": [borrow.id for borrow in borrows]}}, {"$set": {"is_overdue": True}}, **self.db.options()
        )


class Waitlistpository(MongoRepository):
    collection, model = "waitlist", Waitlist

    async def create(self, waitlist: Waitlist):
        return await self._insert(waitlist)

    async def get_by_edition_id(self, edition_id: int):
        return await self._find({"edition_id": edition_id}, ("created_at", 1))

    async def get_by_edition_id_and_user_plan(self, edition_id: int, user_plan: UserPlan):
        for item in await self.get_by_edition_id(edition_id):
            user = await self.db.collection("users").find_one({"_id": item.user_id, "plan": serialize(user_plan)}, **self.db.options())
            if user:
                return item
        return None

    async def get_by_user_id_and_edition_id(self, edition_id: int, user_id: int):
        return await self._find_one({"edition_id": edition_id, "user_id": user_id})

    async def delete(self, waitlist: Waitlist):
        await self._delete(waitlist)


class TransactionRepository(MongoRepository):
    collection, model = "transactions", Transaction
    enum_fields = {"type": __import__("app.transaction.models.enums", fromlist=["TransactionType"]).TransactionType}

    async def create(self, transaction: Transaction):
        return await self._insert(transaction)

    async def get_by_user_id(self, user_id: int):
        return await self._find({"user_id": user_id}, ("date", -1))


class OutboxRepository(MongoRepository):
    collection, model = "outbox_events", OutboxEvent

    async def add(self, event: OutboxEvent):
        if event.created_at is None:
            event.created_at = datetime.utcnow()
        return await self._insert(event)

    async def get_unprocessed(self, limit: int):
        return (await self._find({"processed": False}, ("id", 1)))[:limit]
