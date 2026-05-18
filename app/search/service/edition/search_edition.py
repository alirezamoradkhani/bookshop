from app.search.service.normalize_query import normalize_query
from app.search.service.edition.build_filters import build_filters
from app.search.service.paginate import paginate
from app.search.service.edition.rank_results import rank_results
from app.search.provider.base import SearchProvider


async def search_editions(
    q: str,
    search_provider: SearchProvider,
    book_id=None,
    category=None,
    available=None,
    purchasable=None,
    min_price=None,
    max_price=None,
    page: int = 1,
    size: int = 20
):
    # 1. normalize input
    query = normalize_query(q)

    # 2. build filters
    filters = build_filters(
        book_id=book_id,
        category=category,
        available=available,
        purchasable=purchasable,
        min_price=min_price,
        max_price=max_price
    )

    # 3. call provider (search engine)
    raw_results = await search_provider.search(
        query=query,
        filters=filters,
        index_name="editions"
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