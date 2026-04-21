from app.core.exceptions import AppError
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, email: str, password: str):
        if self.user_repo.get_by_email(email):
            raise AppError("EMAIL_EXISTS", "Email already exists", status_code=400)
        return self.user_repo.create(email=email, password_hash=hash_password(password))

    def login(self, email: str, password: str) -> str:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise AppError("INVALID_CREDENTIALS", "Invalid email or password", status_code=401)
        return create_access_token(str(user.id))
