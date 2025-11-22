from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Sex(Enum):
    male = "male"
    female = "female"


@dataclass
class User:
    id: int
    email: str
    password: str
    created_at: datetime
    name: str | None = None
    sex: Sex | None = None
    age: int | None = None
