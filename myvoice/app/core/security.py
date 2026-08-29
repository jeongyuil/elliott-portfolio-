"""JWT security helpers."""
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import get_settings

settings = get_settings()


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer(auto_error=False) # Allow cookie fallback


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


from fastapi import Request

async def get_token_parent(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    # 1. Check Cookie
    token = request.cookies.get("access_token")
    if token:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        return token
    # 2. Check Header
    if credentials:
        return credentials.credentials
    raise HTTPException(status_code=401, detail="Not authenticated")

async def get_token_child(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    # 1. Check Cookie
    token = request.cookies.get("child_token")
    if token:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        return token
    # 2. Check Header
    if credentials:
        return credentials.credentials
    raise HTTPException(status_code=401, detail="Not authenticated (Child)")


async def get_current_family_id(
    token: str = Depends(get_token_parent),
) -> str:
    """FastAPI dependency: extract family_id from JWT."""
    payload = decode_access_token(token)
    family_id = payload.get("family_id")
    if not family_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return family_id


async def get_current_child_id(
    token: str = Depends(get_token_child),
) -> str:
    """FastAPI dependency: extract child_id from child-scoped JWT (Kids View)."""
    payload = decode_access_token(token)
    child_id = payload.get("child_id")
    if not child_id:
        raise HTTPException(
            status_code=403,
            detail="Child profile not selected. Use /v1/auth/select-child first.",
        )
    return child_id


async def get_current_user_payload(
    token: str = Depends(get_token_parent),
) -> dict:
    """FastAPI dependency: get full token payload."""
    return decode_access_token(token)
