from app.search.provider.base import SearchProvider


class MeiliSearchProvider(SearchProvider):

    def __init__(self, client):
        self.client = client

    def _build_filters(self, filters):
        return " AND ".join(filters) if filters else None

    async def search(self, query, filters, index_name: str):
        index = self.client.index(index_name)

        filter_expr = self._build_filters(filters)

        result = index.search(query, {
        "filter": filter_expr
    })

        return result["hits"]

    async def index(self, index_name: str, doc):
        index = self.client.index(index_name)
        index.add_documents([doc])

    async def delete(self, index_name: str, doc_id: str):
        index = self.client.index(index_name)
        index.delete_document(doc_id)