from app.core.exceptions import AppError
from app.repositories.book_repository import BookRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.user_repository import UserRepository


class ReviewService:
    def __init__(self, review_repo: ReviewRepository, user_repo: UserRepository, book_repo: BookRepository):
        self.review_repo = review_repo
        self.user_repo = user_repo
        self.book_repo = book_repo

    def create(self, payload: dict):
        if not self.user_repo.get_by_id(payload["user_id"]):
            raise AppError("USER_NOT_FOUND", "User not found", status_code=404)
        if not self.book_repo.get(payload["book_id"]):
            raise AppError("BOOK_NOT_FOUND", "Book not found", status_code=404)
        return self.review_repo.create(payload)

    def get(self, review_id: int):
        review = self.review_repo.get(review_id)
        if not review:
            raise AppError("REVIEW_NOT_FOUND", "Review not found", status_code=404)
        return review

    def list(self, page: int, size: int, book_id: int | None, user_id: int | None, rating: int | None):
        return self.review_repo.list(page, size, book_id, user_id, rating)

    def update(self, review_id: int, payload: dict):
        review = self.get(review_id)
        return self.review_repo.update(review, payload)

    def delete(self, review_id: int):
        review = self.get(review_id)
        self.review_repo.delete(review)
