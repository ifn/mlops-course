from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import re


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
    # events: List["Event"] = Relationship(
    #     back_populates="creator",
    #     sa_relationship_kwargs={
    #         "cascade": "all, delete-orphan",
    #         "lazy": "selectin"
    #     }
    # )

    class Config:
        """Model configuration"""

        validate_assignment = True
        arbitrary_types_allowed = True
