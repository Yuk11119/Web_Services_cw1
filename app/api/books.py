from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.core.db import get_db
from app.core.responses import success_response
from app.repositories.author_repository import AuthorRepository
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookOut, BookUpdate
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"], dependencies=[Depends(get_current_user_id)])


def _service(db: Session) -> BookService:
    return BookService(BookRepository(db), AuthorRepository(db))


@router.post("", status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    book = _service(db).create(payload.model_dump())
    return success_response(BookOut.model_validate(book).model_dump())


@router.get("")
def list_books(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    genre: str | None = None,
    year: int | None = None,
    author_id: int | None = None,
    db: Session = Depends(get_db),
):
    rows, total = _service(db).list(page, size, genre, year, author_id)
    return success_response([BookOut.model_validate(x).model_dump() for x in rows], {"page": page, "size": size, "total": total})


@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = _service(db).get(book_id)
    return success_response(BookOut.model_validate(book).model_dump())


@router.put("/{book_id}")
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    book = _service(db).update(book_id, payload.model_dump(exclude_unset=True))
    return success_response(BookOut.model_validate(book).model_dump())


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    _service(db).delete(book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
