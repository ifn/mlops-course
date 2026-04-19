from typing import List, Dict
import logging

from fastapi import APIRouter, HTTPException, Response, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database.database import get_session
from app.models.user import User
from app.models.billing.balance import Balance
from app.auth.hash_password import HashPassword
from app.auth.jwt_handler import create_access_token
from app.services.crud import user as UserService
from app.services.crud.billing import balance as BalanceService
from app.routes.models.user_response import UserResponse
from app.database.config import get_settings


hash_password = HashPassword()


logger = logging.getLogger(__name__)

user_route = APIRouter()


@user_route.get(
    "/",
    response_model=List[UserResponse],
    summary="Get all users",
    response_description="List of all users",
)
async def get_all_users(session=Depends(get_session)) -> List[UserResponse]:
    """
    Get list of all users.

    Args:
        session: Database session

    Returns:
        List[UserResponse]: List of users
    """
    try:
        users = UserService.get_all_users(session)
        logger.info(f"Retrieved {len(users)} users")

        users_resp = [UserResponse.form(user) for user in users]
        return users_resp
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving users",
        )


@user_route.post(
    "/signup",
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="User Registration",
    description="Register a new user with email and password",
)
async def signup(
    data: User,
    session=Depends(get_session),
) -> Dict[str, str]:
    """
    Create new user account.

    Args:
        data: User registration data
        session: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: If user already exists
    """
    try:
        if UserService.get_user_by_email(session, data.email):
            logger.warning(f"Signup attempt with existing email: {data.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        balance = Balance()
        BalanceService.create_balance(session, balance)

        user = User(
            email=data.email,
            password=hash_password.create_hash(data.password),
            balance_id=balance.id,
        )
        UserService.create_user(session, user)

        logger.info(f"New user registered: {data.email}")
        return {"message": "User successfully registered"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user",
        )


@user_route.post("/signin")
async def signin(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session=Depends(get_session),
) -> Dict[str, str]:
    """
    Authenticate existing user.

    Args:
        response: FastAPI response (used to set httpOnly cookie)
        form_data: OAuth2 form with username (email) and password
        session: Database session

    Returns:
        dict: access_token and token_type

    Raises:
        HTTPException: If authentication fails
    """
    user = UserService.get_user_by_email(session, form_data.username)
    if user is None:
        logger.warning(f"Login attempt with non-existent email: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    if not hash_password.verify_hash(form_data.password, user.password):
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials passed",
        )

    access_token = create_access_token(user.email)
    settings = get_settings()
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=f"Bearer {access_token}",
        httponly=True,
    )

    logger.info(f"User signed in: {user.email}")
    return {"access_token": access_token, "token_type": "Bearer"}
