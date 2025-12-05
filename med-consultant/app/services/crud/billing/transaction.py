from typing import List, Optional

from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from models.billing.transaction import FinancialTransaction


# def get_all_llm_queries(session: Session) -> List[LLMQuery]:
#     """
#     Retrieve all llm_queries.

#     Args:
#         session: Database session

#     Returns:
#         List[LLMQuery]: List of all llm_queries
#     """
#     try:
#         statement = select(LLMQuery)
#         llm_queries = session.exec(statement).all()
#         return llm_queries
#     except Exception as e:
#         raise


# def get_llm_query_by_id(session: Session, llm_query_id: int) -> Optional[LLMQuery]:
#     """
#     Get llm_query by ID.

#     Args:
#         llm_query_id: LLMQuery ID to find
#         session: Database session

#     Returns:
#         Optional[LLMQuery]: Found llm_query or None
#     """
#     try:
#         statement = (
#             select(LLMQuery).where(LLMQuery.id == llm_query_id)
#             # ?
#             # .options(
#             #     selectinload(LLMQuery.dialogue),
#             # )
#         )
#         llm_query = session.exec(statement).first()
#         return llm_query
#     except Exception as e:
#         raise


def create_transaction(
    session: Session, transaction: FinancialTransaction,
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


# def delete_llm_query(session: Session, llm_query_id: int) -> bool:
#     """
#     Delete llm_query by ID.

#     Args:
#         llm_query_id: LLMQuery ID to delete
#         session: Database session

#     Returns:
#         bool: True if deleted, False if not found
#     """
#     try:
#         llm_query = get_llm_query_by_id(session, llm_query_id)
#         if not llm_query:
#             return False

#         session.delete(llm_query)
#         session.commit()
#         return True
#     except Exception as e:
#         session.rollback()
#         raise
