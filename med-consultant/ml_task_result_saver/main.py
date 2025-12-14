import json
import logging
from datetime import datetime

import pika
from sqlmodel import Session

# FIXME
from app.models.user import User
from app.models.ml_task import MLTask
from app.models.dialogue import Dialogue
from app.models.llm_query import LLMQuery
from app.models.billing.balance import Balance
from app.models.billing.transaction import FinancialTransaction

from app.models.llm_query import LLMQueryUpdate
from app.models.ml_task import MLTaskStatus
from app.services.crud.llm_query import (
    update_llm_query,
    get_llm_query_by_id,
)
from app.database.database import get_database_engine


QUEUE_NAME = "ml_task_result_queue"


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main() -> None:
    connection_params = pika.ConnectionParameters(
        host="rabbitmq",
        port=5672,
        virtual_host="/",
        credentials=pika.PlainCredentials(
            username="muser",
            password="pass",
        ),
        heartbeat=30,
        blocked_connection_timeout=2,
    )
    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    def callback(ch, method, properties, body):
        logger.info(f"Received: '{body}'")

        llm_req_d = json.loads(body)

        qu = LLMQueryUpdate(
            response=llm_req_d["response"],
            ml_task_status=MLTaskStatus.COMPLETED,
            ml_task_termination_time=datetime.now(),
        )

        engine = get_database_engine()

        with Session(engine) as session:
            q = get_llm_query_by_id(session, llm_req_d["id"])

            update_llm_query(session, q.id, qu)

        # ?
        ch.basic_ack(delivery_tag=method.delivery_tag)

        logger.info(f"Saved: '{qu}'")

    channel.basic_consume(
        queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False
    )

    logger.info("Waiting for messages. To exit, press Ctrl+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
