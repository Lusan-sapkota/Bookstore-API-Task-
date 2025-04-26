from typing import List
from pydantic import BaseModel, field_validator

class BookBase(BaseModel):
    title: str
    author: str
    published_year: int

    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Title must not be empty')
        return v
    
    @field_validator('published_year')
    def published_year_must_be_number(cls, v):
        if not isinstance(v, int):
            raise ValueError('Published year must be a number')
        return v

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True

class PaginatedBooks(BaseModel):
    total: int
    page: int
    size: int
    books: List[Book]