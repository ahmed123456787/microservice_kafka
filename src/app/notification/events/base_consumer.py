import json
import asyncio
import logging
from typing import Any, Dict, Optional
import contextlib
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError


logger = logging.getLogger(__name__)

class AsyncEventConsumer:
    """
    Base class for async Kafka consumers.
    """

    def __init__(self, bootstrap_servers: list, topic: str, group_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id

        self.consumer: Optional[AIOKafkaConsumer] = None
        self.task: Optional[asyncio.Task] = None
        self.running: bool = False

    async def start(self):
        """Start Kafka consumer"""
        if self.running:
            logger.warning(" Consumer already running")
            return

        try:
            self.consumer = AIOKafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode()),
                auto_offset_reset="earliest",
                enable_auto_commit=True,
            )

            logger.info(f"Connecting to Kafka: {self.bootstrap_servers}, topic={self.topic}")
            await self.consumer.start()

            self.running = True
            self.task = asyncio.create_task(self._consume_loop())
            logger.info("Kafka consumer started")

        except Exception as e:
            logger.error(f" Failed to start consumer: {e}", exc_info=True)
            await self.stop()
            raise

    async def stop(self):
        """Gracefully stop Kafka consumer"""
        logger.info("Stopping Kafka consumer...")
        self.running = False

        if self.task:
            self.task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.task

        if self.consumer:
            with contextlib.suppress(Exception):
                await self.consumer.stop()

        logger.info("✅ Kafka consumer stopped")

    async def _consume_loop(self):
        """Main Kafka message loop"""
        logger.info("🔄 Listening for messages...")

        try:
            async for msg in self.consumer:
                if not self.running:
                    break

                logger.debug(f"📩 Msg offset={msg.offset}, partition={msg.partition}")
                await self._process_message(msg.value)

        except asyncio.CancelledError:
            logger.info("↩️ Consumer loop cancelled")
        except KafkaError as e:
            logger.error(f"⚠️ Kafka error: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"❌ Unexpected error in consumer loop: {e}", exc_info=True)

    async def _process_message(self, data: Dict[str, Any]):
        """Call subclass handler"""
        try:
            await self.process_event(data)
        except Exception as e:
            logger.error(f"❌ Error processing event: {data} | {e}", exc_info=True)

    async def process_event(self, event: Dict[str, Any]):
        """To be overridden by child consumers"""
        raise NotImplementedError("Subclasses must implement process_event()")