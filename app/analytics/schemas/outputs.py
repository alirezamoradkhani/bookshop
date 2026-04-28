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