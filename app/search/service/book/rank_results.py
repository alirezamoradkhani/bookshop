def rank_results(items: list, query: str):
    def score(item):
        s = 0

        title = (item.get("title") or "").lower()
        desc = (item.get("description") or "").lower()
        isbn = item.get("isbn")

        if isbn == isbn:
            s += 100

        if query in title:
            s += 50

        if query in desc:
            s += 10

        return s

    return sorted(items, key=score, reverse=True)