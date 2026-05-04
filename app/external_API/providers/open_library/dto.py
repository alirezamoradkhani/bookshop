from pydantic import BaseModel
from typing import List, Optional


class ExternalBookDTO(BaseModel):
    title: str
    authors: List[str] = []
    first_publish_year: Optional[int] = None
    isbn: List[str] = []
    language: List[str] = []
    cover_id: Optional[int] = None
    work_id: Optional[str] = None


class WorkBookDTO(BaseModel):
    work_id: str
    title: str
    description: str | None = None
    subjects: List[str] = []
    author_keys: List[str] = []
    cover_ids: List[int] = []