from pydantic import BaseModel


class Best_edition_in_borrow(BaseModel):
    book_id: int
    book_title: str
    book_category: str
    edition_id: int
    specefic_edition_title: str |None = None
    total_borrow: int

class Best_edition_in_sell(BaseModel):
    book_id: int
    book_title: str
    book_category: str
    edition_id: int
    specefic_edition_title: str |None = None
    total_sales: int

class Best_author_in_income(BaseModel):
    author_id: int
    author_name: str
    total_income: int

class Best_author_in_sell(BaseModel):
    author_id: int
    author_name: str
    total_sales: int