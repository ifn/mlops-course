from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import re


class MLTaskStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class MLTask(SQLModel, table=True):
    id: int
    created_at: datetime
    status: MLTaskStatus = MLTaskStatus.NOT_STARTED
    termination_time: datetime | None = None
