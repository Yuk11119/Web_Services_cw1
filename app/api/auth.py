from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.responses import success_response
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenOut, UserLogin, UserOut, UserRegister
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    service = AuthService(UserRepository(db))
    user = service.register(payload.email, payload.password)
    return success_response(UserOut.model_validate(user).model_dump())


@router.post("/login", response_model=None)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(UserRepository(db))
    token = service.login(payload.email, payload.password)
    return success_response(TokenOut(access_token=token).model_dump())
