import time
from datetime import datetime

from app.database.database import init_db, get_database_engine
from sqlmodel import Session

from app.models.user import User
from app.models.ml_task import (
    MLTask,
    MLTaskStatus,
)
from app.models.dialogue import Dialogue
from app.models.llm_query import LLMQuery, LLMQueryUpdate
from app.models.billing.balance import Balance
from app.models.billing.transaction import FinancialTransaction, TransactionFactory
from app.services.crud.user import (
    create_user,
    get_all_users,
)
from app.services.crud.dialogue import (
    create_dialogue,
    get_all_dialogues,
)
from app.services.crud.llm_query import (
    create_llm_query,
    update_llm_query,
    get_llm_query_by_id,
)
from app.services.crud.billing.balance import (
    create_balance,
)
from app.services.crud.billing.transaction import (
    create_transaction,
    get_all_transactions,
    get_transaction_by_id,
)


def main() -> None:
    init_db(drop_all=True)
    print("Init db finished successfully")

    engine = get_database_engine()

    with Session(engine) as session:
        print("-" * 100)
        print("Balance:")
        print("-" * 100)

        balanceA = Balance()
        balanceB = Balance()
        create_balance(session, balanceA)
        print(balanceA)
        create_balance(session, balanceB)
        print(balanceB)

        print("-" * 100)
        print("Users:")
        print("-" * 100)

        userA = User(
            email="manA@mail.tr",
            password="123456",
            balance_id=balanceA.id,
        )
        userB = User(
            email="ivan@mail.ru",
            password="123456",
            balance_id=balanceB.id,
        )
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

        qu = LLMQueryUpdate(
            response="""Knee pain after playing basketball can be caused by various factors such as overuse, improper technique or training methods, or underlying medical conditions.
1. Overuse: Prolonged repetitive strain on your knees can cause tendinitis (inflammation of the tendons) or a stress fracture in the surrounding bones.
2. Improper Technique: Playing basketball without proper form or landing awkwardly after jumps may put excessive force on your knee joint, causing ligament sprains or meniscal tears.
3. Underlying Conditions: Existing medical conditions such as osteoarthritis, patellofemoral pain syndrome (kneecap pain), or a previous injury can contribute to post-game knee pain.""",
            ml_task_status=MLTaskStatus.COMPLETED,
            ml_task_termination_time=datetime.now(),
        )
        update_llm_query(session, q2.id, qu)

        q2up = get_llm_query_by_id(session, query2.id)
        print(q2up)
        print(q2up.ml_task)

        print("-" * 100)
        print("Financial transactions:")
        print("-" * 100)

        dep = TransactionFactory.create_deposit(10, userA.id)
        create_transaction(session, dep)
        print(dep)
        print(dep.user.balance)
        dep2 = TransactionFactory.create_deposit(8, userA.id)
        create_transaction(session, dep2)
        print(dep2)
        print(userA.balance)
        dep.approve()
        print(userA.balance)
        dep2.approve()
        print(userA.balance)
        wd = TransactionFactory.create_withdrawal(2, userA.id)
        create_transaction(session, wd)
        print(wd)
        wd.approve()
        print(userA.balance)

        print(userB.balance)

        print(get_all_transactions(session))
        print(get_transaction_by_id(session, 3))

    print("entering loop ...")
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
