from app.dependency_injection.container import Container

container = Container()
def setup_book_indexes():
    client = container.meili_client()

    # --- create index (idempotent) ---
    try:
        client.get_index("books")
        print("books index already exists")
    except Exception:
        client.create_index("books", {"primaryKey": "id"})
        print("books index created")

    index = client.index("books")

    # --- schema config ---
    index.update_searchable_attributes([
        "title",
        "author_name"
    ])

    index.update_filterable_attributes([
        "author_id",
        "category",
        "available"
    ])

    index.update_sortable_attributes([
        "id"
    ])

    print("books index configured")


def setup_edition_indexes():
    client = container.meili_client()

    # --- create index (idempotent) ---
    try:
        client.get_index("editions")
        print("editions index already exists")
    except Exception:
        client.create_index("editions", {"primaryKey": "id"})
        print("editions index created")

    index = client.index("editions")

    # --- searchable fields (برای full-text search) ---
    index.update_searchable_attributes([
        "edition_title",
        "isbn",
        "description",

        # book fields (denormalized)
        "book_title",
        "book_author_names",
        "book_category",
    ])

    # --- filterable fields (برای فیلتر دقیق) ---
    index.update_filterable_attributes([
        "book_id",
        "price",
        "amount",
        "available",
        "purchasable",

        # اگر می‌خوای فیلتر category هم بزنی
        "book_category",
    ])

    # --- sortable fields (برای sort کردن نتایج) ---
    index.update_sortable_attributes([
        "price",
        "amount",
    ])

    print("editions index configured")


if __name__ == "__main__":
    setup_book_indexes()
    setup_edition_indexes()
