from typing import List, Dict
import logging

from fastapi import APIRouter, HTTPException, status, Depends

from database.database import get_session
from models.user import User
from models.billing.balance import Balance
from services.crud import user as UserService
from services.crud.billing import balance as BalanceService
from routes.models.user_response import UserResponse


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
            password=data.password,
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
    data: User,
    session=Depends(get_session),
) -> User:
    """
    Authenticate existing user.

    Args:
        form_data: User credentials
        session: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: If authentication fails
    """
    user = UserService.get_user_by_email(session, data.email)
    if user is None:
        logger.warning(f"Login attempt with non-existent email: {data.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    if user.password != data.password:
        logger.warning(f"Failed login attempt for user: {data.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed",
        )

    return user
