import unittest

from app.book.repo.book import BookRepository


class FakeCollection:
    def __init__(self, document):
        self.document = document
        self.updates = []

    async def find_one(self, query, **options):
        return self.document

    async def update_one(self, query, update, **options):
        self.updates.append((query, update, options))


class FakeDatabase:
    def __init__(self, collection):
        self.collection = collection

    def __getitem__(self, name):
        return self.collection


class MongoRepositoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_read_does_not_write_and_update_is_explicit(self):
        collection = FakeCollection(
            {
                "_id": 7,
                "id": 7,
                "title": "Old title",
                "is_deleted": False,
                "external_provider": None,
                "external_id": None,
                "author_ids": [],
                "categories": [],
            }
        )
        repository = BookRepository(FakeDatabase(collection), lambda: None)

        book = await repository.get_by_id(7)

        self.assertEqual(collection.updates, [])

        await repository.update_book_title(book, "New title")

        self.assertEqual(book.title, "New title")
        self.assertEqual(
            collection.updates,
            [({"_id": 7}, {"$set": {"title": "New title"}}, {})],
        )


if __name__ == "__main__":
    unittest.main()
