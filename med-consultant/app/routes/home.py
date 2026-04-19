from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth.hash_password import HashPassword
from app.auth.jwt_handler import create_access_token, verify_access_token
from app.database.config import get_settings
from app.database.database import get_session
from app.services.auth.loginform import LoginForm
from app.services.crud import user as UserService

home_route = APIRouter()
hash_password = HashPassword()
templates = Jinja2Templates(directory="view")


@home_route.get("/auth/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse(request, "login.html", {"errors": []})


@home_route.post("/auth/login", response_class=HTMLResponse)
async def login_post(request: Request, session=Depends(get_session)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            user = UserService.get_user_by_email(session, form.username)
            if user and hash_password.verify_hash(form.password, user.password):
                access_token = create_access_token(user.email)
                settings = get_settings()
                response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
                response.set_cookie(
                    key=settings.COOKIE_NAME,
                    value=f"Bearer {access_token}",
                    httponly=True,
                )
                return response
            form.errors.append("Incorrect email or password")
        except Exception:
            form.errors.append("Incorrect email or password")
    return templates.TemplateResponse(request, "login.html", {"errors": form.errors})


@home_route.get("/auth/logout")
async def logout():
    settings = get_settings()
    response = RedirectResponse(url="/")
    response.delete_cookie(settings.COOKIE_NAME)
    return response


@home_route.get("/", response_class=HTMLResponse)
async def index(request: Request):
    settings = get_settings()
    token = request.cookies.get(settings.COOKIE_NAME)
    user = None
    if token:
        try:
            raw = token.removeprefix("Bearer ")
            user = verify_access_token(raw)["user"]
        except Exception:
            pass
    return templates.TemplateResponse(request, "index.html", {"user": user})


@home_route.get(
    "/health",
    response_model=Dict[str, str],
    summary="Health check endpoint",
    description="Returns service health status",
)
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for monitoring.

    Returns:
        Dict[str, str]: Health status message

    Raises:
        HTTPException: If service is unhealthy
    """
    try:
        # Add actual health checks here
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service unavailable")
