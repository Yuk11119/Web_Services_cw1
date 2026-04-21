import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone

from app.core.config import settings

try:
    from jose import JWTError, jwt  # type: ignore
except Exception:  # pragma: no cover
    JWTError = Exception
    jwt = None

try:
    from passlib.context import CryptContext  # type: ignore
except Exception:  # pragma: no cover
    CryptContext = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") if CryptContext else None


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    pad = "=" * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode(data + pad)


def _fallback_hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return f"pbkdf2_sha256${salt}${digest.hex()}"


def _fallback_verify_password(password: str, encoded: str) -> bool:
    try:
        _, salt, digest_hex = encoded.split("$", 2)
    except ValueError:
        return False
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return hmac.compare_digest(digest.hex(), digest_hex)


def hash_password(password: str) -> str:
    if pwd_context:
        return pwd_context.hash(password)
    return _fallback_hash_password(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if pwd_context:
        return pwd_context.verify(plain_password, hashed_password)
    return _fallback_verify_password(plain_password, hashed_password)


def _fallback_create_token(subject: str) -> str:
    exp = int((datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)).timestamp())
    payload = {"sub": subject, "exp": exp}
    payload_b = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    payload_enc = _b64url_encode(payload_b)
    sig = hmac.new(settings.jwt_secret_key.encode("utf-8"), payload_enc.encode("utf-8"), hashlib.sha256).digest()
    return f"fallback.{payload_enc}.{_b64url_encode(sig)}"


def _fallback_decode_token(token: str) -> str | None:
    try:
        prefix, payload_enc, sig_enc = token.split(".", 2)
        if prefix != "fallback":
            return None
        expected_sig = hmac.new(settings.jwt_secret_key.encode("utf-8"), payload_enc.encode("utf-8"), hashlib.sha256).digest()
        if not hmac.compare_digest(_b64url_encode(expected_sig), sig_enc):
            return None
        payload = json.loads(_b64url_decode(payload_enc).decode("utf-8"))
        if int(payload.get("exp", 0)) < int(datetime.now(timezone.utc).timestamp()):
            return None
        return payload.get("sub")
    except Exception:
        return None


def create_access_token(subject: str) -> str:
    if jwt is not None:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        payload = {"sub": subject, "exp": expire}
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return _fallback_create_token(subject)


def decode_access_token(token: str) -> str | None:
    if jwt is not None:
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            return payload.get("sub")
        except JWTError:
            return None
    return _fallback_decode_token(token)
