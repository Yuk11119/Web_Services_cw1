from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.exceptions import AppError
from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_current_user_id(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> int:
    if not token:
        raise AppError("AUTH_REQUIRED", "Authentication required", status_code=401)
    subject = decode_access_token(token)
    if not subject:
        raise AppError("INVALID_TOKEN", "Invalid or expired token", status_code=401)
    user = UserRepository(db).get_by_id(int(subject))
    if not user:
        raise AppError("USER_NOT_FOUND", "User not found", status_code=401)
    return user.id
