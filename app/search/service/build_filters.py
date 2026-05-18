def build_filters(author_id=None, category=None):
    filters = []

    if author_id:
        filters.append(f"author_id = {author_id}")

    if category:
        filters.append(f"category = '{category}'")

    return filters