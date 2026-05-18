from app.search.provider.base import SearchProvider


class MeiliSearchProvider(SearchProvider):

    def __init__(self, client):
        self.client = client

    async def search(self, query, filters, index_name: str):
        index = self.client.index(index_name)

        result = index.search(query, {
            "filter": self._build_filters(filters)
        })

        return result["hits"]

    async def index(self, index_name: str, doc):
        index = self.client.index(index_name)
        index.add_documents([doc])

    async def delete(self, index_name: str, doc_id: str):
        index = self.client.index(index_name)
        index.delete_document(doc_id)

    def _build_filters(self, filters):
        # ساده نگه داشتیم
        return []