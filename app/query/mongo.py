from __future__ import annotations

from typing import Any


class MongoRow(dict):
    @property
    def _mapping(self):
        return self


async def aggregate(db, collection: str, pipeline: list[dict[str, Any]]) -> list[MongoRow]:
    cursor = db[collection].aggregate(pipeline)
    return [MongoRow(document) async for document in cursor]


async def best_user_in_buy(db):
    return await aggregate(db, "order_editions", [
        {"$match": {"state": "done"}},
        {"$lookup": {"from": "orders", "localField": "order_id", "foreignField": "_id", "as": "order"}},
        {"$unwind": "$order"},
        {"$group": {"_id": "$order.user_id", "total_buys": {"$sum": 1}}},
        {"$lookup": {"from": "users", "localField": "_id", "foreignField": "_id", "as": "user"}},
        {"$unwind": "$user"},
        {"$project": {"_id": 0, "user_id": "$_id", "user_name": "$user.username", "user_plan": "$user.plan", "total_buys": 1}},
        {"$sort": {"total_buys": -1}},
        {"$limit": 20},
    ])


async def best_category_in_sell(db):
    return await aggregate(db, "order_editions", [
        {"$match": {"state": "done"}},
        {"$lookup": {"from": "editions", "localField": "edition_id", "foreignField": "_id", "as": "edition"}},
        {"$unwind": "$edition"},
        {"$lookup": {"from": "books", "localField": "edition.book_id", "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$unwind": "$book.categories"},
        {"$group": {"_id": "$book.categories", "total_sales": {"$sum": 1}}},
        {"$project": {"_id": 0, "category": "$_id", "total_sales": 1}},
        {"$sort": {"total_sales": -1}},
    ])


async def best_edition_in_sell(db):
    return await aggregate(db, "order_editions", [
        {"$match": {"state": "done"}},
        {"$group": {"_id": "$edition_id", "total_sales": {"$sum": 1}}},
        {"$sort": {"total_sales": -1}},
        {"$lookup": {"from": "editions", "localField": "_id", "foreignField": "_id", "as": "edition"}},
        {"$unwind": "$edition"},
        {"$lookup": {"from": "books", "localField": "edition.book_id", "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$project": {"_id": 0, "book_id": "$book._id", "book_title": "$book.title", "book_category": {"$arrayElemAt": ["$book.categories", 0]}, "edition_id": "$_id", "specefic_edition_title": "$edition.specefic_edition_title", "total_sales": 1}},
    ])


async def best_edition_in_borrow(db):
    return await aggregate(db, "borrows", [
        {"$group": {"_id": "$edition_id", "total_borrow": {"$sum": 1}}},
        {"$sort": {"total_borrow": -1}},
        {"$lookup": {"from": "editions", "localField": "_id", "foreignField": "_id", "as": "edition"}},
        {"$unwind": "$edition"},
        {"$lookup": {"from": "books", "localField": "edition.book_id", "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$project": {"_id": 0, "book_id": "$book._id", "book_title": "$book.title", "book_category": {"$arrayElemAt": ["$book.categories", 0]}, "edition_id": "$_id", "specefic_edition_title": "$edition.specefic_edition_title", "total_borrow": 1}},
    ])


async def best_author_in_sell(db):
    return await aggregate(db, "order_editions", [
        {"$match": {"state": "done"}},
        {"$lookup": {"from": "editions", "localField": "edition_id", "foreignField": "_id", "as": "edition"}},
        {"$unwind": "$edition"},
        {"$lookup": {"from": "books", "localField": "edition.book_id", "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$unwind": "$book.author_ids"},
        {"$group": {"_id": "$book.author_ids", "total_sales": {"$sum": 1}}},
        {"$lookup": {"from": "users", "localField": "_id", "foreignField": "_id", "as": "author"}},
        {"$unwind": "$author"},
        {"$project": {"_id": 0, "author_id": "$_id", "author_name": "$author.username", "total_sales": 1}},
        {"$sort": {"total_sales": -1}},
    ])


async def best_author_in_income(db):
    return await aggregate(db, "order_editions", [
        {"$match": {"state": "done"}},
        {"$lookup": {"from": "editions", "localField": "edition_id", "foreignField": "_id", "as": "edition"}},
        {"$unwind": "$edition"},
        {"$lookup": {"from": "books", "localField": "edition.book_id", "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$unwind": "$book.author_ids"},
        {"$group": {"_id": "$book.author_ids", "total_income": {"$sum": "$price"}}},
        {"$lookup": {"from": "users", "localField": "_id", "foreignField": "_id", "as": "author"}},
        {"$unwind": "$author"},
        {"$project": {"_id": 0, "author_id": "$_id", "author_name": "$author.username", "total_income": 1}},
        {"$sort": {"total_income": -1}},
    ])


async def count_of_owerdue(db, user):
    return await db["borrows"].count_documents({"user_id": user.id, "is_overdue": True})


async def user_with_over_due(db):
    return await aggregate(db, "borrows", [
        {"$match": {"is_overdue": True, "status": "active"}},
        {"$lookup": {"from": "users", "localField": "user_id", "foreignField": "_id", "as": "user"}},
        {"$unwind": "$user"},
        {"$project": {"_id": 0, "user_id": "$user._id", "user_name": "$user.username", "borrow_id": "$_id", "borrow_start": "$borrowed_at", "borrow_end": "$due_at"}},
    ])


async def monthly_income(db, user):
    rows = await aggregate(db, "order_editions", [
        {"$match": {"state": "done"}},
        {"$group": {"_id": None, "monthly_income": {"$sum": "$price"}}},
        {"$project": {"_id": 0, "monthly_income": 1}},
    ])
    return rows[0] if rows else None
