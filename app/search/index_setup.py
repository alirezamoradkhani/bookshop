from app.dependency_injection.container import Container

container = Container()
def setup_indexes():
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


if __name__ == "__main__":
    setup_indexes()