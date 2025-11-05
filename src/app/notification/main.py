from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import base, engine
from config.config import AppConfig
from events.consumer import UserEventConsumer
import logging
import sys


# Configure logging FIRST
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Create  consumer instance
event_consumer = UserEventConsumer(
    bootstrap_servers=AppConfig.KAFKA_BOOTSTRAP_SERVERS,
    topic=AppConfig.KAFKA_NOTIFICATION_TOPIC,
    group_id="testing"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan with proper startup/shutdown"""

    #apply migrations.
    base.metadata.create_all(bind=engine)

    # Startup
    logger.info("=" * 50)
    logger.info("🚀 Starting FastAPI application...")
    logger.info(f"Kafka servers: {AppConfig.KAFKA_BOOTSTRAP_SERVERS}")
    logger.info(f"Kafka topic: {AppConfig.KAFKA_NOTIFICATION_TOPIC}")
    logger.info("=" * 50)
    
    try:
        await event_consumer.start()
        logger.info("✅ Application startup complete")
    except Exception as e:
        logger.error(f" Failed to start consumer: {e}", exc_info=True)
        raise
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("=" * 50)
    logger.info("🛑 Shutting down FastAPI application...")
    logger.info("=" * 50)
    try:
        await event_consumer.stop()
        logger.info("✅ Application shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=True)



app = FastAPI(
    title="Notification Service",
    lifespan=lifespan,
    docs_url="/docs" if AppConfig.DEBUG else None,
    redoc_url="/redoc" if AppConfig.DEBUG else None,
    openapi_url="/openapi.json" if AppConfig.DEBUG else None
)




@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok", 
        "message": "Notification service is running.",
        "consumer_running": event_consumer.running,
        "kafka_servers": AppConfig.KAFKA_BOOTSTRAP_SERVERS,
        "kafka_topic": AppConfig.KAFKA_NOTIFICATION_TOPIC
    }