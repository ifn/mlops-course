from datetime import datetime

from models.user import (
    User,
)
from models.llm_query import (
    Dialogue,
    LLMQuery,
)


def main() -> None:
    user = User(
        id=1,
        email="manA@mail.tr",
        password="123456",
        created_at=datetime.now(),
    )

    dialogue = Dialogue(
        id=1,
        user_id=user.id,
        created_at=datetime.now(),
    )

    query = LLMQuery(
        dialogue_id=dialogue.id,
        query="i feel pain in my knee after basketball. what are the reasons?",
        ml_task_id=1,
        ml_task_created_at=datetime.now(),
    )

    print(f"Created user: {user}")
    print(f"Dialogue: {dialogue}")
    print(f"Query: {query}")
    print(f"Query processing status: {query.status}")


if __name__ == "__main__":
    main()
