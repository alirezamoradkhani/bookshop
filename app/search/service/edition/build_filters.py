def build_filters(
    book_id=None,
    category=None,
    available=None,
    purchasable=None,
    min_price=None,
    max_price=None
):
    filters = []

    if book_id:
        filters.append(f"book_id = {book_id}")

    if category:
        filters.append(f"book_category = '{category}'")

    if available is True:
        filters.append("available = true")
    elif available is False:
        filters.append("available = false")

    if purchasable is True:
        filters.append("purchasable = true")
    elif purchasable is False:
        filters.append("purchasable = false")

    if min_price is not None:
        filters.append(f"price >= {min_price}")

    if max_price is not None:
        filters.append(f"price <= {max_price}")

    return filters