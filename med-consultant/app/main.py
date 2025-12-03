import time

from database.database import init_db, get_database_engine
from sqlmodel import Session

from models.user import User
from models.ml_task import (
    MLTask,
)
from models.dialogue import Dialogue
from models.llm_query import LLMQuery
from models.billing import Balance
from services.crud.user import (
    create_user,
    get_all_users,
)
from services.crud.dialogue import (
    create_dialogue,
    get_all_dialogues,
)
from services.crud.llm_query import (
    create_llm_query,
    get_llm_query_by_id,
)


def main() -> None:
    userA = User(
        email="manA@mail.tr",
        password="123456",
    )
    userB = User(
        email="ivan@mail.ru",
        password="123456",
    )

    init_db(drop_all=True)
    print("Init db finished successfully")

    engine = get_database_engine()

    with Session(engine) as session:
        print("-" * 100)
        print("Users:")
        print("-" * 100)

        create_user(session, userA)
        print(userA)
        create_user(session, userB)
        print(userB)
        users = get_all_users(session)
        print(users)

        print("-" * 100)
        print("Dialogues:")
        print("-" * 100)

        dialogueA1 = Dialogue(
            user_id=userA.id,
        )
        dialogueA2 = Dialogue(
            user_id=userA.id,
        )

        create_dialogue(session, dialogueA1)
        print(dialogueA1)
        print(dialogueA1.user)
        create_dialogue(session, dialogueA2)
        print(dialogueA2)
        print(dialogueA2.user)
        print(userA.dialogues)
        dialogues = get_all_dialogues(session)
        print(dialogues)

        print("-" * 100)
        print("Queries:")
        print("-" * 100)

        query1 = LLMQuery(
            user_id=userA.id,
            dialogue_id=dialogueA1.id,
            query="i feel pain in my knee after basketball. what are the reasons?",
        )
        create_llm_query(session, query1)
        print(query1)
        print(query1.dialogue)
        query2 = LLMQuery(
            user_id=userA.id,
            dialogue_id=dialogueA1.id,
            query='how can i check "Meniscal tears" version?',
        )
        create_llm_query(session, query2)
        print(query2)
        print(query2.dialogue)
        print(dialogueA1.queries)

        q2 = get_llm_query_by_id(session, query2.id)
        print(q2.dialogue.queries)
        print(q2.ml_task)

    print("entering loop ...")
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
