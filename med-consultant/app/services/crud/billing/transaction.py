from typing import List, Optional

from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from models.billing.transaction import FinancialTransaction


def get_all_transactions(session: Session) -> List[FinancialTransaction]:
    """
    Retrieve all transactions.

    Args:
        session: Database session

    Returns:
        List[FinancialTransaction]: List of all transactions
    """
    try:
        statement = select(FinancialTransaction)
        transactions = session.exec(statement).all()
        return transactions
    except Exception as e:
        raise


def get_transaction_by_id(
    session: Session,
    transaction_id: int,
) -> Optional[FinancialTransaction]:
    """
    Get transaction by ID.

    Args:
        transaction_id: FinancialTransaction ID to find
        session: Database session

    Returns:
        Optional[FinancialTransaction]: Found transaction or None
    """
    try:
        statement = (
            select(FinancialTransaction)
            .where(FinancialTransaction.id == transaction_id)
            .options(
                selectinload(FinancialTransaction.balance),
            )
        )
        transaction = session.exec(statement).first()
        return transaction
    except Exception as e:
        raise


def create_transaction(
    session: Session,
    transaction: FinancialTransaction,
) -> FinancialTransaction:
    """
    Create new financial transaction.

    Args:
        transaction: FinancialTransaction to create
        session: Database session

    Returns:
        FinancialTransaction: Created transaction with ID
    """
    try:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction
    except Exception as e:
        session.rollback()
        raise


def delete_transaction(
    session: Session,
    transaction_id: int,
) -> bool:
    """
    Delete transaction by ID.

    Args:
        transaction_id: FinancialTransaction ID to delete
        session: Database session

    Returns:
        bool: True if deleted, False if not found
    """
    try:
        transaction = get_transaction_by_id(session, transaction_id)
        if not transaction:
            return False

        session.delete(transaction)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise
