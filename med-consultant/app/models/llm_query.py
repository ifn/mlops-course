from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

# ?
from app.models.ml_task import MLTaskStatus

if TYPE_CHECKING:
    from app.models.ml_task import MLTask, MLTaskStatus
    from app.models.user import User
    from app.models.dialogue import Dialogue


class LLMQueryUpdate(SQLModel):
    response: Optional[str] = None
    ml_task_status: Optional["MLTaskStatus"] = None
    ml_task_termination_time: Optional[datetime] = None


class LLMQuery(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    query: str
    response: Optional[str] = None

    # 3NF violation
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="queries")

    dialogue_id: Optional[int] = Field(foreign_key="dialogue.id")
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

    def update(self, llm_query_update: LLMQueryUpdate):
        self.response = llm_query_update.response
        self.ml_task.status = llm_query_update.ml_task_status
        self.ml_task.termination_time = llm_query_update.ml_task_termination_time
