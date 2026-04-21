from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    isbn: str = Field(min_length=10, max_length=20)
    publication_year: int | None = Field(default=None, ge=0, le=2100)
    genre: str | None = Field(default=None, max_length=100)
    page_count: int | None = Field(default=None, ge=1)
    author_id: int


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    isbn: str | None = Field(default=None, min_length=10, max_length=20)
    publication_year: int | None = Field(default=None, ge=0, le=2100)
    genre: str | None = Field(default=None, max_length=100)
    page_count: int | None = Field(default=None, ge=1)
    author_id: int | None = None


class BookOut(BaseModel):
    id: int
    title: str
    isbn: str
    publication_year: int | None
    genre: str | None
    page_count: int | None
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
