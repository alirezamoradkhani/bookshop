def rank_results(items: list, query: str):

    def score(item):
        s = 0

        edition_title = (item.get("edition_title") or "").lower()
        book_title = (item.get("book_title") or "").lower()
        description = (item.get("description") or "").lower()
        isbn = item.get("isbn")

        price = item.get("price")
        available = item.get("available")
        purchasable = item.get("purchasable")

        # 1. ISBN match (خیلی مهم‌ترین signal)
        if isbn and query == str(isbn).lower():
            s += 200

        # 2. exact match in edition title
        if query in edition_title:
            s += 80

        # 3. match in book title
        if query in book_title:
            s += 60

        # 4. match in description
        if query in description:
            s += 20

        # 5. business boost
        if available:
            s += 10

        if purchasable:
            s += 30

        return s

    return sorted(items, key=score, reverse=True)