from .event import UserCreatedEvent
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError
from typing import Any, Dict
import json
import asyncio
import logging

logger = logging.getLogger(__name__)

class AsyncEventConsumer:
    def __init__(self, bootstrap_servers: list, topic: str, group_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
        self.running = False
        self.consumer_task = None
        
    async def start(self):
        """Start the Kafka consumer"""
        if self.running:
            logger.warning("Consumer is already running")
            return
            
        try:
            self.running = True
            
            logger.info(f"Creating Kafka consumer for topic '{self.topic}' with servers: {self.bootstrap_servers}")
            
            self.consumer = AIOKafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                # Add these for better debugging
                request_timeout_ms=30000,
                session_timeout_ms=10000,
                heartbeat_interval_ms=3000,
            )
            
            logger.info("Starting Kafka consumer connection...")
            await self.consumer.start()
            logger.info(f"✅ Successfully connected to Kafka and subscribed to topic: {self.topic}")
            
            # Start consuming in background
            self.consumer_task = asyncio.create_task(self._consume_events())
            logger.info("✅ Kafka consumer task started and running")
            
        except KafkaError as e:
            logger.error(f"❌ Kafka connection error: {e}", exc_info=True)
            self.running = False
            raise
        except Exception as e:
            logger.error(f"❌ Error starting consumer: {e}", exc_info=True)
            self.running = False
            raise
    
    async def stop(self):
        """Stop the Kafka consumer"""
        logger.info("Stopping Kafka consumer...")
        self.running = False
        
        if self.consumer_task:
            self.consumer_task.cancel()
            try:
                await self.consumer_task
            except asyncio.CancelledError:
                logger.info("Consumer task cancelled successfully")
        
        if self.consumer:
            try:
                await self.consumer.stop()
                logger.info("✅ Kafka consumer stopped successfully")
            except Exception as e:
                logger.error(f"Error stopping consumer: {e}")
    
    async def _consume_events(self):
        """Main consumer loop"""
        logger.info("🔄 Starting consumer loop, waiting for messages...")
        
        try:
            message_count = 0
            async for message in self.consumer:
                if not self.running:
                    logger.info("Consumer stopping, breaking loop")
                    break
                
                message_count += 1
                logger.info(f"📨 Received message #{message_count} from partition {message.partition}, offset {message.offset}")
                
                try:
                    event_data = message.value
                    logger.debug(f"Message content: {event_data}")
                    await self.process_event(event_data)
                    logger.info(f"✅ Successfully processed message #{message_count}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"❌ JSON decode error: {e}", exc_info=True)
                except Exception as e:
                    logger.error(f"❌ Error processing message: {e}", exc_info=True)
                    
        except asyncio.CancelledError:
            logger.info("Consumer task cancelled")
            raise
        except Exception as e:
            logger.error(f"❌ Error in consumer loop: {e}", exc_info=True)
            raise
        finally:
            logger.info(f"Consumer loop ended. Total messages processed: {message_count}")
    
    async def process_event(self, event_data: Dict[str, Any]):
        """Override this method to handle events"""
        raise NotImplementedError("Subclasses must implement process_event()")


class UserEventConsumer(AsyncEventConsumer):
    async def process_event(self, event_data: Dict[str, Any]):
        """Process incoming events based on event_type"""
        if not self.running:
            return
            
        logger.info(f"🔍 Processing event: {event_data}")
        
        try:
            if all(field in event_data for field in ['user_id', 'username', 'email']):
                event = UserCreatedEvent(**event_data)
                await self._handle_user_created(event)
            else:
                logger.warning(f"⚠️ Unknown event format (missing required fields): {event_data}")
                
        except Exception as e:
            logger.error(f"❌ Error parsing event: {e}", exc_info=True)
    
    async def _handle_user_created(self, event: UserCreatedEvent):
        """Handle UserCreatedEvent"""
        if not self.running:
            return
            
        logger.info(f"👤 User created: {event.username} ({event.email}) - ID: {event.user_id}")
        # Add your notification logic here