def paginate(items: list, page: int, size: int):
    start = (page - 1) * size
    end = start + size
    return items[start:end]