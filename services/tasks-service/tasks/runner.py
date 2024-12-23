import asyncio
import json
from datetime import datetime

from confluent_kafka import Message  # type: ignore # noqa: PGH003
from pydantic import BaseModel, ValidationError

from tasks.logger import logger


class UserCreatedMessage(BaseModel):
    id: str
    email: str
    createdAt: str
    updatedAt: str

async def handle_user_created(msg: Message) -> None:
    try:
        logger.info("Processing user created message")
        deserialized: dict = json.loads(msg.value().decode("utf-8"))
        data = UserCreatedMessage.model_validate(deserialized)
        logger.info(f"id: {data.id}")
        logger.info(f"email: {data.email}")
        logger.info(f"createdAt: {datetime.fromisoformat(data.createdAt)}")
        await asyncio.sleep(10) # Fake processing time
        logger.info("Data processed")
    except ValidationError as e:
        logger.error(e, exc_info=True)
        return
