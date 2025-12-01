from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.ml_task import MLTask, MLTaskStatus
    from models.dialogue import Dialogue


class LLMQuery(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    query: str
    response: Optional[str] = None
    dialogue_id: int = Field(foreign_key="dialogue.id")
    dialogue: Optional["Dialogue"] = Relationship(back_populates="queries")
    ml_task_id: Optional[int] = Field(foreign_key="mltask.id")
    ml_task: Optional["MLTask"] = Relationship(back_populates="llm_query")

    @property
    def created_at(self) -> Optional[datetime]:
        return self.ml_task.created_at if self.ml_task else None

    @property
    def status(self) -> Optional["MLTaskStatus"]:
        return self.ml_task.status if self.ml_task else None

    @property
    def termination_time(self) -> Optional[datetime]:
        return self.ml_task.termination_time if self.ml_task else None
