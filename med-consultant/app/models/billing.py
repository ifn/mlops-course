from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import re

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class Balance(SQLModel, table=True):
    id: int
    user_id: int
    amount: int
    updated_at: datetime


class FinancialTransaction(SQLModel, table=True):
    id: int
    balance_id: int
    amount: int
    created_at: datetime
