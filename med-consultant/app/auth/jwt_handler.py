from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError

from app.database.config import get_settings


def create_access_token(user: str) -> str:
    settings = get_settings()
    payload = {
        "user": user,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def verify_access_token(token: str) -> dict:
    settings = get_settings()
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
