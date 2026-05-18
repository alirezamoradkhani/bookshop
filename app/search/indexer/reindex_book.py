from app.dependency_injection.container import Container

async def reindex_books():
    container = Container()
    client = container.meili_client()

    index = client.index("books")

    uow = container.uow
    async with uow() as uow:

        books = await uow.book.get_all()

        docs = []

        for book in books:
            docs.append({
                "id": book.id,
                "title": book.title,
                "author_name": [a.username for a in await uow.author.get_by_ids([b.author_id for b in await uow.bookauthor.get_by_book_id(book.id)])],
                "category": [c.category for c in await uow.bookcategory.get_by_book_id(book.id)],
                "available": not book.is_deleted
            })

    index.add_documents(docs)

    print(f"reindexed {len(docs)} books")

if __name__ == "__main__":
    import asyncio
    asyncio.run(reindex_books())