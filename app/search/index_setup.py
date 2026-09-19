import logging

logger = logging.getLogger(__name__)

from app.dependency_injection.container import Container

container = Container()
def setup_book_indexes():
    client = container.meili_client()

    # --- create index (idempotent) ---
    try:
        client.get_index("books")
        logger.debug("Books index already exists")
    except Exception:
        client.create_index("books", {"primaryKey": "id"})
        logger.debug("Books index created")

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

    logger.debug("Books index configured")


def setup_edition_indexes():
    client = container.meili_client()

    # --- create index (idempotent) ---
    try:
        client.get_index("editions")
        logger.debug("Editions index already exists")
    except Exception:
        client.create_index("editions", {"primaryKey": "id"})
        logger.debug("Editions index created")

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

    logger.debug("Editions index configured")


if __name__ == "__main__":
    setup_book_indexes()
    setup_edition_indexes()
