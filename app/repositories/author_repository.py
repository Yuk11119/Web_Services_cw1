from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.author import Author


class AuthorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: dict) -> Author:
        author = Author(**payload)
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author

    def get(self, author_id: int) -> Author | None:
        return self.db.get(Author, author_id)

    def list(self, page: int, size: int) -> tuple[list[Author], int]:
        total = self.db.scalar(select(func.count()).select_from(Author)) or 0
        rows = self.db.scalars(select(Author).offset((page - 1) * size).limit(size)).all()
        return rows, total

    def update(self, author: Author, payload: dict) -> Author:
        for k, v in payload.items():
            setattr(author, k, v)
        self.db.commit()
        self.db.refresh(author)
        return author

    def delete(self, author: Author) -> None:
        self.db.delete(author)
        self.db.commit()
