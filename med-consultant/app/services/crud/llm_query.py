from typing import List, Optional

from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.models.llm_query import LLMQuery, LLMQueryUpdate
from app.models.ml_task import MLTask


def get_all_llm_queries(session: Session) -> List[LLMQuery]:
    """
    Retrieve all llm_queries.

    Args:
        session: Database session

    Returns:
        List[LLMQuery]: List of all llm_queries
    """
    try:
        statement = select(LLMQuery)
        llm_queries = session.exec(statement).all()
        return llm_queries
    except Exception as e:
        raise


def get_llm_query_by_id(session: Session, llm_query_id: int) -> Optional[LLMQuery]:
    """
    Get llm_query by ID.

    Args:
        llm_query_id: LLMQuery ID to find
        session: Database session

    Returns:
        Optional[LLMQuery]: Found llm_query or None
    """
    try:
        statement = (
            select(LLMQuery).where(LLMQuery.id == llm_query_id)
            # ?
            # .options(
            #     selectinload(LLMQuery.dialogue),
            # )
        )
        llm_query = session.exec(statement).first()
        return llm_query
    except Exception as e:
        raise


def create_llm_query(session: Session, llm_query: LLMQuery) -> LLMQuery:
    """
    Create new llm_query.

    Args:
        llm_query: LLMQuery to create
        session: Database session

    Returns:
        LLMQuery: Created llm_query with ID
    """
    try:
        ml_task = MLTask()

        session.add(ml_task)
        session.flush()

        llm_query.ml_task_id = ml_task.id

        session.add(llm_query)
        session.commit()
        session.refresh(llm_query)
        return llm_query
    except Exception as e:
        session.rollback()
        raise


def update_llm_query(
    session: Session,
    llm_query_id: int,
    llm_query_update: LLMQueryUpdate,
) -> Optional[LLMQuery]:
    """
    Update existing llm_query.

    Args:
        session: Database session
        llm_query_id: LLMQuery ID to update
        llm_query_update: LLMQueryUpdate object

    Returns:
        Optional[LLMQuery]: Updated llm_query or None if not found
    """
    try:
        llm_query = get_llm_query_by_id(session, llm_query_id)
        if not llm_query:
            return None

        llm_query.update(llm_query_update)

        session.add(llm_query)
        session.commit()
        session.refresh(llm_query)
        return llm_query
    except Exception as e:
        session.rollback()
        raise


def delete_all_llm_queries(session: Session) -> int:
    """
    Delete all llm_queries.

    Args:
        session: Database session

    Returns:
        int: Number of deleted llm_queries
    """
    try:
        statement = select(LLMQuery)
        llm_queries = session.exec(statement).all()
        count = len(llm_queries)

        for llm_query in llm_queries:
            session.delete(llm_query)

        session.commit()
        return count
    except Exception as e:
        session.rollback()
        raise


def delete_llm_query(session: Session, llm_query_id: int) -> bool:
    """
    Delete llm_query by ID.

    Args:
        llm_query_id: LLMQuery ID to delete
        session: Database session

    Returns:
        bool: True if deleted, False if not found
    """
    try:
        llm_query = get_llm_query_by_id(session, llm_query_id)
        if not llm_query:
            return False

        session.delete(llm_query)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise
