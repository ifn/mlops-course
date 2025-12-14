import logging
import json

import pika

from app.rabbitmq.client import publish_message


QUEUE_NAME_IN = "ml_task_queue"
QUEUE_NAME_OUT = "ml_task_result_queue"


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

    channel.queue_declare(queue=QUEUE_NAME_IN)

    def callback(ch, method, properties, body):
        logger.info(f"Received: '{body}'")

        # create ollama request
        resp = "dummy"

        llm_req_d = json.loads(body)
        llm_req_d["response"] = resp
        llm_req_js = json.dumps(llm_req_d)

        publish_message(QUEUE_NAME_OUT, llm_req_js)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        logger.info(f"Sent: '{llm_req_js}'")

    channel.basic_consume(
        queue=QUEUE_NAME_IN,
        on_message_callback=callback,
        auto_ack=False,
    )

    logger.info("Waiting for messages. To exit, press Ctrl+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
