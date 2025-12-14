from typing import List, Optional

from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.models.billing.balance import Balance


def create_balance(session: Session, balance: Balance) -> Balance:
    """
    Create new llm_query.

    Args:
        llm_query: LLMQuery to create
        session: Database session

    Returns:
        LLMQuery: Created llm_query with ID
    """
    try:
        session.add(balance)
        session.commit()
        session.refresh(balance)
        return balance
    except Exception as e:
        session.rollback()
        raise
