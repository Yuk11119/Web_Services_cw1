from app.core.exceptions import AppError
from app.repositories.author_repository import AuthorRepository


class AuthorService:
    def __init__(self, author_repo: AuthorRepository):
        self.author_repo = author_repo

    def create(self, payload: dict):
        return self.author_repo.create(payload)

    def get(self, author_id: int):
        author = self.author_repo.get(author_id)
        if not author:
            raise AppError("AUTHOR_NOT_FOUND", "Author not found", status_code=404)
        return author

    def list(self, page: int, size: int):
        return self.author_repo.list(page, size)

    def update(self, author_id: int, payload: dict):
        author = self.get(author_id)
        return self.author_repo.update(author, payload)

    def delete(self, author_id: int):
        author = self.get(author_id)
        self.author_repo.delete(author)
