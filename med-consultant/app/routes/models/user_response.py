from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.user import User, Sex


class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str] = None
    sex: Optional[Sex] = None
    age: Optional[int] = None
    created_at: datetime
    balance: float

    @staticmethod
    def form(user: User):
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            sex=user.sex,
            age=user.age,
            created_at=user.created_at,
            balance=user.balance.amount,
        )
