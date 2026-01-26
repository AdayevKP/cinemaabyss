import logging
import os
from aiokafka import AIOKafkaConsumer  # type: ignore


logger = logging.getLogger(__name__)


KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "kafka:9092")


async def consume():
    consumer = AIOKafkaConsumer(
        "movie-events",
        "user-events",
        "payment-events",
        bootstrap_servers=KAFKA_BROKERS,
    )

    await consumer.start()
    try:
        async for msg in consumer:
            logger.info(f"Consumer msg: {msg}")
    except Exception as e:
        logger.error(f"Error in Kafka consumer: {e}")
    finally:
        await consumer.stop()
        logger.info("Consumer stopped")