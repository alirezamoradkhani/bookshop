def normalize_query(q: str) -> str:
    if not q:
        return ""

    return q.strip().lower()