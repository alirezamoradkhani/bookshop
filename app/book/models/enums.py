from enum import Enum


class Category(str, Enum):
    SCIENCE = "science"
    ART = "art"
    HISTORY = "history"
    TECHNOLOGY = "technology"
    PROGRAMMING = "programming"
    BUSINESS = "business"
    LITERATURE = "literature"

