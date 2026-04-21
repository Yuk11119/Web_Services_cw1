from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.review import Review


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: dict) -> Review:
        review = Review(**payload)
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def get(self, review_id: int) -> Review | None:
        return self.db.get(Review, review_id)

    def list(self, page: int, size: int, book_id: int | None, user_id: int | None, rating: int | None) -> tuple[list[Review], int]:
        stmt = select(Review)
        count_stmt = select(func.count()).select_from(Review)
        if book_id:
            stmt = stmt.where(Review.book_id == book_id)
            count_stmt = count_stmt.where(Review.book_id == book_id)
        if user_id:
            stmt = stmt.where(Review.user_id == user_id)
            count_stmt = count_stmt.where(Review.user_id == user_id)
        if rating:
            stmt = stmt.where(Review.rating == rating)
            count_stmt = count_stmt.where(Review.rating == rating)

        total = self.db.scalar(count_stmt) or 0
        rows = self.db.scalars(stmt.offset((page - 1) * size).limit(size)).all()
        return rows, total

    def update(self, review: Review, payload: dict) -> Review:
        for k, v in payload.items():
            setattr(review, k, v)
        self.db.commit()
        self.db.refresh(review)
        return review

    def delete(self, review: Review) -> None:
        self.db.delete(review)
        self.db.commit()
