from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING, Protocol
from abc import abstractmethod

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.user import User
    from models.billing.balance import Balance


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class TransactionStrategy(Protocol):
    @abstractmethod
    def is_permitted(self, balance: "Balance", amount: float) -> bool:
        pass

    @abstractmethod
    def apply(self, balance: "Balance", amount: float) -> None:
        pass


class DepositStrategy:
    def is_permitted(self, balance: "Balance", amount: float) -> bool:
        return True

    def apply(self, balance: "Balance", amount: float) -> None:
        balance.amount += amount


class WithdrawalStrategy:
    def is_permitted(self, balance: "Balance", amount: float) -> bool:
        return (balance.amount - amount) > 0

    def apply(self, balance: "Balance", amount: float) -> None:
        balance.amount -= amount


class FinancialTransaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: TransactionType = Field(index=True)
    amount: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="transactions")

    @property
    def _strategy(self) -> TransactionStrategy:
        return {
            TransactionType.DEPOSIT: DepositStrategy(),
            TransactionType.WITHDRAWAL: WithdrawalStrategy(),
        }[self.type]

    def is_permitted(self) -> bool:
        return self._strategy.is_permitted(self.user.balance, self.amount)

    def approve(self) -> None:
        self._strategy.apply(self.user.balance, self.amount)
        self.user.balance.updated_at = self.created_at


class TransactionFactory:
    @staticmethod
    def create_deposit(amount: float, user_id: int) -> FinancialTransaction:
        return FinancialTransaction(
            type=TransactionType.DEPOSIT,
            amount=amount,
            user_id=user_id,
        )

    @staticmethod
    def create_withdrawal(amount: float, user_id: int) -> FinancialTransaction:
        return FinancialTransaction(
            type=TransactionType.WITHDRAWAL,
            amount=amount,
            user_id=user_id,
        )
