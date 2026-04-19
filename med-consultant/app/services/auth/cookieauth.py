from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel

from app.database.config import get_settings


class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    OAuth2 password flow that reads the token from a cookie instead of
    the Authorization header.
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        auto_error: bool = True,
    ):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": {}})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        settings = get_settings()
        authorization: str = request.cookies.get(settings.COOKIE_NAME)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None
        return param
