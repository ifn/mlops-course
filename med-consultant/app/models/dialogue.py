from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON

if TYPE_CHECKING:
    from models.user import User
    from models.llm_query import LLMQuery


class Dialogue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user_id: Optional[int] = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="dialogues")

    queries: List["LLMQuery"] = Relationship(back_populates="dialogue")

    topics: List[str] = Field(
        sa_column=Column(JSON),
        default_factory=list,
    )
