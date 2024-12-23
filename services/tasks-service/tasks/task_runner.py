import asyncio
import json
import os
import random
from tasks.kafka import Producer
from typing import Optional

from confluent_kafka import Message  # type: ignore # noqa: PGH003
from pydantic import BaseModel, ValidationError

from tasks.logger import logger


class TaskCreatedMessage(BaseModel):
    id: str
    userId: str
    status: Optional[str] = None

async def handle_task_created(msg: Message) -> None:
    try:
        producer = Producer(uri=os.getenv("KAFKA_URI"))
        logger.info("Processing Task created message")
        deserialized: dict = json.loads(msg.value().decode("utf-8"))
        data = TaskCreatedMessage.model_validate(deserialized)
        logger.info(f"id: {data.id}")
        await asyncio.sleep(10)
        data.status = "RUNNING"
        producer.send_json("task.updated", {"id": data.id, "status": data.status})
        await asyncio.sleep(20)
        data.status = random.choice(['SUCCESS', 'FAILED'])
        producer.send_json("task.updated", {"id": data.id, "status": data.status})
    except ValidationError as e:
        logger.error(e, exc_info=True)
        return
