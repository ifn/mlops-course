from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


@dataclass
class Balance:
    id: int
    user_id: int
    amount: int
    updated_at: datetime


@dataclass
class FinancialTransaction:
    id: int
    balance_id: int
    amount: int
    created_at: datetime
