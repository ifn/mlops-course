import time

from database.database import init_db, get_database_engine
from sqlmodel import Session

from models.user import User
from models.ml_task import (
    MLTask,
)
from models.dialogue import Dialogue
from models.llm_query import LLMQuery
from models.billing.balance import Balance
from models.billing.transaction import FinancialTransaction, TransactionFactory
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
from services.crud.billing.balance import (
    create_balance,
)
from services.crud.billing.transaction import (
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
