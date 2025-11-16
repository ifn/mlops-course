from datetime import datetime

from models.llm_query import (
    Dialogue,
    LLMQuery,
    User,
)


def main() -> None:
    user = User(
        id=1,
        email="manA@mail.tr",
        created_at=datetime.now(),
    )

    dialogue = Dialogue(
        id=1,
        user_id=user.id,
        created_at=datetime.now(),
    )

    query = LLMQuery(
        id=1,
        query="i feel pain in my knee after basketball. what are the reasons?",
        created_at=datetime.now(),
        dialogue_id=dialogue.id,
    )

    print(f"Created user: {user}")
    print(f"Dialogue: {dialogue}")
    print(f"Query: {query.query}")


if __name__ == "__main__":
    main()
