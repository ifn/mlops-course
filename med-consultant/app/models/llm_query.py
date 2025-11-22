from dataclasses import dataclass, field, InitVar
from datetime import datetime

from .ml_task import MLTask, MLTaskStatus


@dataclass
class Dialogue:
    id: int
    user_id: int
    created_at: datetime
    topics: list[str] = field(default_factory=list)


@dataclass
class LLMQuery:
    dialogue_id: int
    query: str
    response: str | None = None

    _ml_task: MLTask = field(init=False)
    ml_task_id: InitVar[int | None] = None
    ml_task_created_at: InitVar[datetime | None] = None

    def __post_init__(
        self,
        ml_task_id: int,
        ml_task_created_at: datetime,
    ):
        self._ml_task = MLTask(
            id=ml_task_id,
            created_at=ml_task_created_at,
        )

    @property
    def id(self) -> int:
        return self._ml_task.id

    @property
    def created_at(self) -> datetime:
        return self._ml_task.created_at

    @property
    def status(self) -> MLTaskStatus:
        return self._ml_task.status

    @property
    def termination_time(self) -> datetime | None:
        return self._ml_task.termination_time
