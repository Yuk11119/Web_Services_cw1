from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.review import Review


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def genre_trends(self, start_year: int | None, end_year: int | None):
        stmt = (
            select(
                Book.genre,
                func.count(Book.id).label("book_count"),
                func.round(func.avg(Review.rating), 2).label("avg_rating"),
            )
            .select_from(Book)
            .join(Review, Review.book_id == Book.id, isouter=True)
            .group_by(Book.genre)
            .order_by(func.count(Book.id).desc())
        )
        if start_year is not None:
            stmt = stmt.where(Book.publication_year >= start_year)
        if end_year is not None:
            stmt = stmt.where(Book.publication_year <= end_year)

        return [
            {"genre": row.genre, "book_count": row.book_count, "avg_rating": row.avg_rating}
            for row in self.db.execute(stmt).all()
        ]

    def rating_distribution(self):
        stmt = (
            select(Review.rating, func.count(Review.id).label("count"))
            .group_by(Review.rating)
            .order_by(Review.rating)
        )
        return [{"rating": row.rating, "count": row.count} for row in self.db.execute(stmt).all()]

    def recommendations(self, user_id: int, limit: int = 5):
        user_top_genres = (
            select(Book.genre)
            .join(Review, Review.book_id == Book.id)
            .where(Review.user_id == user_id)
            .group_by(Book.genre)
            .order_by(func.avg(Review.rating).desc())
            .limit(3)
            .subquery()
        )
        reviewed_books = select(Review.book_id).where(Review.user_id == user_id).subquery()

        stmt = (
            select(
                Book.id.label("book_id"),
                Book.title,
                Book.genre,
                (
                    func.coalesce(func.avg(Review.rating), 0)
                    + case((Book.genre.in_(select(user_top_genres.c.genre)), 1.0), else_=0.0)
                ).label("score"),
            )
            .select_from(Book)
            .join(Review, Review.book_id == Book.id, isouter=True)
            .where(~Book.id.in_(select(reviewed_books.c.book_id)))
            .group_by(Book.id, Book.title, Book.genre)
            .order_by(func.coalesce(func.avg(Review.rating), 0).desc())
            .limit(limit)
        )
        return [
            {"book_id": row.book_id, "title": row.title, "genre": row.genre, "score": float(row.score)}
            for row in self.db.execute(stmt).all()
        ]
