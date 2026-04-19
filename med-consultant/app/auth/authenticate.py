from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth.jwt_handler import verify_access_token
from app.services.auth.cookieauth import OAuth2PasswordBearerWithCookie


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/signin")
oauth2_scheme_cookie = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/login")


async def authenticate(token: str = Depends(oauth2_scheme)) -> str:
    """Authenticate via Authorization: Bearer header."""
    decoded = verify_access_token(token)
    return decoded["user"]


async def authenticate_cookie(token: str = Depends(oauth2_scheme_cookie)) -> str:
    """Authenticate via httpOnly cookie."""
    decoded = verify_access_token(token)
    return decoded["user"]
