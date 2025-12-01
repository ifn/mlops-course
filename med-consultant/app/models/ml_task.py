from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.llm_query import LLMQuery


class MLTaskStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class MLTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: MLTaskStatus = Field(default=MLTaskStatus.NOT_STARTED)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    termination_time: Optional[datetime] = None

    llm_query: Optional["LLMQuery"] = Relationship(back_populates="ml_task")
