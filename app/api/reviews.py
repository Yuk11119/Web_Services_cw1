from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.core.db import get_db
from app.core.responses import success_response
from app.repositories.book_repository import BookRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.user_repository import UserRepository
from app.schemas.review import ReviewCreate, ReviewOut, ReviewUpdate
from app.services.review_service import ReviewService

router = APIRouter(prefix="/reviews", tags=["reviews"], dependencies=[Depends(get_current_user_id)])


def _service(db: Session) -> ReviewService:
    return ReviewService(ReviewRepository(db), UserRepository(db), BookRepository(db))


@router.post("", status_code=status.HTTP_201_CREATED)
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)):
    review = _service(db).create(payload.model_dump())
    return success_response(ReviewOut.model_validate(review).model_dump())


@router.get("")
def list_reviews(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    book_id: int | None = None,
    user_id: int | None = None,
    rating: int | None = Query(default=None, ge=1, le=5),
    db: Session = Depends(get_db),
):
    rows, total = _service(db).list(page, size, book_id, user_id, rating)
    return success_response([ReviewOut.model_validate(x).model_dump() for x in rows], {"page": page, "size": size, "total": total})


@router.put("/{review_id}")
def update_review(review_id: int, payload: ReviewUpdate, db: Session = Depends(get_db)):
    review = _service(db).update(review_id, payload.model_dump(exclude_unset=True))
    return success_response(ReviewOut.model_validate(review).model_dump())


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    _service(db).delete(review_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
