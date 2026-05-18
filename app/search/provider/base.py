from abc import ABC, abstractmethod
from typing import Any, Dict, List


class SearchProvider(ABC):

    @abstractmethod
    async def search(self, query: str, filters: Dict[str, Any], index_name: str) -> List[Dict]:
        pass

    @abstractmethod
    async def index(self, index_name: str, doc: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def delete(self, index_name: str, doc_id: str) -> None:
        pass