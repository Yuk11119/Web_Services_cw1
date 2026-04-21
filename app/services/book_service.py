from app.core.exceptions import AppError
from app.repositories.author_repository import AuthorRepository
from app.repositories.book_repository import BookRepository


class BookService:
    def __init__(self, book_repo: BookRepository, author_repo: AuthorRepository):
        self.book_repo = book_repo
        self.author_repo = author_repo

    def create(self, payload: dict):
        if self.book_repo.get_by_isbn(payload["isbn"]):
            raise AppError("ISBN_EXISTS", "ISBN already exists", status_code=409)
        if not self.author_repo.get(payload["author_id"]):
            raise AppError("AUTHOR_NOT_FOUND", "Author not found", status_code=404)
        return self.book_repo.create(payload)

    def get(self, book_id: int):
        book = self.book_repo.get(book_id)
        if not book:
            raise AppError("BOOK_NOT_FOUND", "Book not found", status_code=404)
        return book

    def list(self, page: int, size: int, genre: str | None, year: int | None, author_id: int | None):
        return self.book_repo.list(page, size, genre, year, author_id)

    def update(self, book_id: int, payload: dict):
        book = self.get(book_id)
        if payload.get("isbn") and payload["isbn"] != book.isbn:
            if self.book_repo.get_by_isbn(payload["isbn"]):
                raise AppError("ISBN_EXISTS", "ISBN already exists", status_code=409)
        if payload.get("author_id") and not self.author_repo.get(payload["author_id"]):
            raise AppError("AUTHOR_NOT_FOUND", "Author not found", status_code=404)
        return self.book_repo.update(book, payload)

    def delete(self, book_id: int):
        book = self.get(book_id)
        self.book_repo.delete(book)
