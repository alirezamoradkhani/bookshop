from app.search.service.normalize_query import normalize_query
from app.search.service.build_filters import build_filters
from app.search.service.paginate import paginate
from app.search.service.rank_results import rank_results
from app.search.provider.base import SearchProvider


async def search_books(
    q: str,
    search_provider: SearchProvider,
    author_id=None,
    category=None,
    page: int = 1,
    size: int = 20
):
    # 1. normalize input
    query = normalize_query(q)

    # 2. build filters
    filters = build_filters(author_id, category)

    # 3. call provider (search engine)
    raw_results = await search_provider.search(
        query=query,
        filters=filters,
        index_name="books"
    )

    # 4. rank results
    ranked = rank_results(raw_results, query)

    # 5. paginate
    paginated = paginate(ranked, page, size)

    return {
        "query": query,
        "total": len(raw_results),
        "page": page,
        "size": size,
        "items": paginated
    }