from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MLTaskStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class MLTask:
    id: int
    created_at: datetime
    status: MLTaskStatus = MLTaskStatus.NOT_STARTED
    termination_time: datetime | None = None
