from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.core.db import get_db
from app.core.responses import success_response
from app.repositories.author_repository import AuthorRepository
from app.schemas.author import AuthorCreate, AuthorOut, AuthorUpdate
from app.services.author_service import AuthorService

router = APIRouter(prefix="/authors", tags=["authors"], dependencies=[Depends(get_current_user_id)])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_author(payload: AuthorCreate, db: Session = Depends(get_db)):
    author = AuthorService(AuthorRepository(db)).create(payload.model_dump())
    return success_response(AuthorOut.model_validate(author).model_dump())


@router.get("")
def list_authors(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    rows, total = AuthorService(AuthorRepository(db)).list(page, size)
    return success_response([AuthorOut.model_validate(x).model_dump() for x in rows], {"page": page, "size": size, "total": total})


@router.get("/{author_id}")
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = AuthorService(AuthorRepository(db)).get(author_id)
    return success_response(AuthorOut.model_validate(author).model_dump())


@router.put("/{author_id}")
def update_author(author_id: int, payload: AuthorUpdate, db: Session = Depends(get_db)):
    author = AuthorService(AuthorRepository(db)).update(author_id, payload.model_dump(exclude_unset=True))
    return success_response(AuthorOut.model_validate(author).model_dump())


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    AuthorService(AuthorRepository(db)).delete(author_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
