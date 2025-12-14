from contextlib import closing
import logging

import pika


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def publish_message(queue_name, message_body):
    try:
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

        with closing(pika.BlockingConnection(connection_params)) as connection:
            channel = connection.channel()

            channel.queue_declare(queue=queue_name)

            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )

            logger.info(f"Message published to queue '{queue_name}': {message_body}")

    except Exception as e:
        logger.error(f"Failed to publish message: {e}")
        raise
