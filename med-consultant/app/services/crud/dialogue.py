from typing import List, Optional

from sqlmodel import Session, select

from app.models.dialogue import Dialogue


def get_all_dialogues(session: Session) -> List[Dialogue]:
    """
    Retrieve all dialogues.

    Args:
        session: Database session

    Returns:
        List[Dialogue]: List of all dialogues
    """
    try:
        statement = select(Dialogue)
        dialogues = session.exec(statement).all()
        return dialogues
    except Exception as e:
        raise


def get_dialogue_by_id(session: Session, dialogue_id: int) -> Optional[Dialogue]:
    """
    Get dialogue by ID.

    Args:
        dialogue_id: Dialogue ID to find
        session: Database session

    Returns:
        Optional[Dialogue]: Found dialogue or None
    """
    try:
        statement = select(Dialogue).where(Dialogue.id == dialogue_id)
        dialogue = session.exec(statement).first()
        return dialogue
    except Exception as e:
        raise


def create_dialogue(session: Session, dialogue: Dialogue) -> Dialogue:
    """
    Create new dialogue.

    Args:
        dialogue: Dialogue to create
        session: Database session

    Returns:
        Dialogue: Created dialogue with ID
    """
    try:
        session.add(dialogue)
        session.commit()
        session.refresh(dialogue)
        return dialogue
    except Exception as e:
        session.rollback()
        raise


def delete_all_dialogues(session: Session) -> int:
    """
    Delete all dialogues.

    Args:
        session: Database session

    Returns:
        int: Number of deleted dialogues
    """
    try:
        statement = select(Dialogue)
        dialogues = session.exec(statement).all()
        count = len(dialogues)

        for dialogue in dialogues:
            session.delete(dialogue)

        session.commit()
        return count
    except Exception as e:
        session.rollback()
        raise


def delete_dialogue(session: Session, dialogue_id: int) -> bool:
    """
    Delete dialogue by ID.

    Args:
        dialogue_id: Dialogue ID to delete
        session: Database session

    Returns:
        bool: True if deleted, False if not found
    """
    try:
        dialogue = get_dialogue_by_id(dialogue_id, session)
        if not dialogue:
            return False

        session.delete(dialogue)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise
