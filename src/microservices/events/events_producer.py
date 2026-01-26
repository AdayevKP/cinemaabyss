import json
import os
import uuid
from datetime import datetime
from typing import Any

from aiokafka import AIOKafkaProducer  # type: ignore
from aiokafka.errors import KafkaError  # type: ignore


KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "kafka:9092")

producer = AIOKafkaProducer(
    bootstrap_servers=KAFKA_BROKERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def _add_meta(event_data: dict[str, Any]) -> dict[str, Any]:
    return {
        **event_data,
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
    }


async def connect() -> None:
    await producer.start()


async def disconnect() -> None:
    await producer.stop()


async def _send(topic: str, event_data: dict[str, Any]) -> dict[str, Any]:
    try:
        metadata = await producer.send_and_wait(topic, _add_meta(event_data))
        return {
            "status": "success",
            "partition": metadata.partition,
            "offset": metadata.offset,
            "event": event_data,
        }
    except KafkaError as e:
        return {"status": "error", "error": str(e), "event": event_data}


async def send_movie_event(event_data: dict[str, Any]) -> dict[str, Any]:
    return await _send("movie-events", event_data)


async def send_user_event(event_data: dict[str, Any]) -> dict[str, Any]:
    return await _send("user-events", event_data)


async def send_payment_event(event_data: dict[str, Any]) -> dict[str, Any]:
    return await _send("payment-events", event_data)
