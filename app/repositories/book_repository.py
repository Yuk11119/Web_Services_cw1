from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.book import Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: dict) -> Book:
        book = Book(**payload)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def get(self, book_id: int) -> Book | None:
        return self.db.get(Book, book_id)

    def get_by_isbn(self, isbn: str) -> Book | None:
        return self.db.scalar(select(Book).where(Book.isbn == isbn))

    def list(self, page: int, size: int, genre: str | None, year: int | None, author_id: int | None) -> tuple[list[Book], int]:
        stmt = select(Book)
        count_stmt = select(func.count()).select_from(Book)
        if genre:
            stmt = stmt.where(Book.genre == genre)
            count_stmt = count_stmt.where(Book.genre == genre)
        if year:
            stmt = stmt.where(Book.publication_year == year)
            count_stmt = count_stmt.where(Book.publication_year == year)
        if author_id:
            stmt = stmt.where(Book.author_id == author_id)
            count_stmt = count_stmt.where(Book.author_id == author_id)

        total = self.db.scalar(count_stmt) or 0
        rows = self.db.scalars(stmt.offset((page - 1) * size).limit(size)).all()
        return rows, total

    def update(self, book: Book, payload: dict) -> Book:
        for k, v in payload.items():
            setattr(book, k, v)
        self.db.commit()
        self.db.refresh(book)
        return book

    def delete(self, book: Book) -> None:
        self.db.delete(book)
        self.db.commit()
