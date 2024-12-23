import json
import os
from typing import Any, Awaitable, Callable

import confluent_kafka  # type: ignore  # noqa: PGH003

from tasks.logger import logger

AsyncCallback = Callable[[Any], Awaitable[Any]]
KAFKA_URI = os.getenv("KAFKA_URI")
if not KAFKA_URI:
    raise ValueError("Missing KAFKA_URI environment variable")

class Producer:
    _broker: confluent_kafka.Producer

    def __init__(self, uri: str) -> None:
        conf = {
            "bootstrap.servers": uri,
            "message.max.bytes": 100e6,
            "session.timeout.ms": 6000,
            "heartbeat.interval.ms": 2000,
            "group.instance.id": "tasks-service-1",
            "partition.assignment.strategy":  "cooperative-sticky",
            "auto.offset.reset": "error",
            "enable.auto.offset.store": False,
            "enable.auto.commit": False,
            "default.topic.config": {"auto.offset.reset": "smallest"},
        }
        self._broker = confluent_kafka.Producer(conf, logger=logger)

        try:
            self._broker.list_topics()
        except confluent_kafka.cimpl.KafkaException as e:
            logger.error(
                f"Failed to connect to Kafka: {e}",
            )
            raise e

    def send_json(
        self,
        topic: str,
        data: dict,
    ) -> None:
        stringified = json.dumps(data)
        try:
            self._broker.produce(
                topic,
                stringified.encode("utf-8"),
                callback=self.delivery_report,
            )
        except confluent_kafka.cimpl.KafkaException as e:
            logger.error(e)
            logger.error(
                f"Failed to produce message: {e} on topic `{topic}`.",
            )
        # Commit the message to the broker
        self._broker.poll(0)
        self._broker.flush()

    def delivery_report(
        self,
        err: confluent_kafka.cimpl.KafkaError,
        msg: confluent_kafka.cimpl.Message,
    ) -> None:
        if err:
            logger.error(
                f"Failed to produce message: {err}",
            )
        else:
            logger.info(
                "Message delivered",
                extra={
                    "topic": msg.topic(),
                    "partition": msg.partition(),
                    "offset": msg.offset(),
                    "size": len(msg.value()),
                },
            )

def on_assign_cb( _consumer: confluent_kafka.Consumer, partitions: list[confluent_kafka.TopicPartition]) -> None:
    logger.info(f"Assigning {len(partitions)} partitions")

async def consume(group_id: str, callback: AsyncCallback, topics: list[str]):
    conf = {
            "bootstrap.servers": KAFKA_URI,
            "message.max.bytes": 100e6,
            "session.timeout.ms": 6000,
            "heartbeat.interval.ms": 2000,
            "group.id": group_id,
            "group.instance.id": "tasks-service-1",
            "partition.assignment.strategy":  "cooperative-sticky",
            "default.topic.config": {"auto.offset.reset": "smallest"},
        }

    logger.info(f"Polling for messages on topics {', '.join(topics)}")

    consumer = confluent_kafka.Consumer(conf)
    consumer.subscribe(topics, on_assign=on_assign_cb)

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == confluent_kafka.KafkaError._PARTITION_EOF:
                    # End of partition event
                    continue
                logger.error(msg.error())
                break

            logger.debug(
                "Message received",
                extra={
                    "topic": msg.topic(),
                    "partition": msg.partition(),
                    "offset": msg.offset(),
                    "size": len(msg.value()),
                },
            )
            await callback(msg) # Simulate async processing
            consumer.commit(msg)
            logger.debug(
                "Message committed",
                extra={
                    "topic": msg.topic(),
                    "partition": msg.partition(),
                    "offset": msg.offset(),
                    "size": len(msg.value()),
                },
            )
    except KeyboardInterrupt:
        pass
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


producer = Producer(KAFKA_URI)
