from datetime import datetime
from enum import Enum
from typing import List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.dialogue import Dialogue
    from app.models.llm_query import LLMQuery
    from app.models.billing.balance import Balance
    from app.models.billing.transaction import FinancialTransaction


class Sex(Enum):
    male = "male"
    female = "female"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(..., unique=True, index=True, min_length=5, max_length=255)
    password: str = Field(..., min_length=4)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    name: str | None = None
    sex: Sex | None = None
    age: int | None = None

    queries: List["LLMQuery"] = Relationship(
        back_populates="user",
    )
    dialogues: List["Dialogue"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"},
    )
    transactions: List["FinancialTransaction"] = Relationship(
        back_populates="user",
    )

    balance_id: int = Field(foreign_key="balance.id")
    balance: "Balance" = Relationship(back_populates="user")

    class Config:
        """Model configuration"""

        validate_assignment = True
        arbitrary_types_allowed = True
