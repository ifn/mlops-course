from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Sex(Enum):
    male = "male"
    female = "female"


@dataclass
class User:
    id: int
    email: str
    created_at: datetime
    name: str | None = None
    sex: Sex | None = None
    age: int | None = None


@dataclass
class Dialogue:
    id: int
    user_id: int
    created_at: datetime
    topics: list[str] = field(default_factory=list)


@dataclass
class LLMQuery:
    id: int
    query: str
    created_at: datetime
    dialogue_id: int
    response: str | None = None
    processing_time: float | None = None
