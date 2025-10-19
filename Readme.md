# Event-Driven Microservices Architecture

A microservices application built with Python FastAPI, implementing event-driven architecture using Apache Kafka for inter-service communication, with centralized logging via Fluentd.

## 🏗️ Architecture Overview

This project demonstrates a modern microservices architecture with the following key components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Service  │    │Notification Svc │    │   Fluentd       │
│   (FastAPI)     │    │   (FastAPI)     │    │  (Logging)      │
└─────────┬───────┘    └─────────┬───────┘    └─────────────────┘
          │                      │                      ▲
          │                      │                      │
          ▼                      ▼                      │
┌─────────────────────────────────────────────────────────────────┐
│                    Apache Kafka                                 │
│              (Event Streaming Platform)                        │
└─────────────────────────────────────────────────────────────────┘
          ▲
          │
┌─────────┴───────┐
│   Zookeeper     │
│ (Kafka Coord.)  │
└─────────────────┘
```

## 🚀 Services

### 1. User Service (`src/app/user/`)

- **Technology**: FastAPI + SQLAlchemy + SQLite
- **Port**: 8000
- **Responsibilities**:
  - User CRUD operations (Create, Read, Update, Delete)
  - User authentication and session management
  - Publishes user events to Kafka
  - Structured logging via Fluentd

**Key Features**:

- RESTful API endpoints (`/users/`)
- User registration with validation (Pydantic schemas)
- Role-based access (Admin, User, Guest)
- Session token management
- Event publishing on user creation

### 2. Notification Service (`src/app/notification/`)

- **Technology**: FastAPI + Clean Architecture
- **Responsibilities**:
  - Send notifications (Email, SMS, Push)
  - Consume user events from Kafka
  - Multiple notification adapters (SendGrid, SMS, Push)

**Key Features**:

- Hexagonal architecture with ports and adapters
- Multiple notification types with validation
- SendGrid integration for email notifications
- Event-driven notification triggering

### 3. Infrastructure Services

#### Apache Kafka

- **Purpose**: Event streaming and inter-service communication
- **Port**: 9092 (external), 9093 (internal)
- **Topics**: `notification`, `user_created`

#### Zookeeper

- **Purpose**: Kafka cluster coordination
- **Port**: 2181

#### Fluentd

- **Purpose**: Centralized log aggregation
- **Port**: 24224
- **Features**: Structured JSON logging from all services

## 📁 Project Structure

```
event_arch/
├── docker-compose.dev.yml          # Development environment setup
├── docker-compose.prod.yml         # Production environment setup
├── Makefile                        # Build and run commands
├── test.py                         # Kafka consumer test script
├── src/app/
│   ├── user/                       # User microservice
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── models.py               # SQLAlchemy database models
│   │   ├── schema.py               # Pydantic validation schemas
│   │   ├── producer.py             # Kafka message producer
│   │   ├── database.py             # Database connection setup
│   │   ├── logging.py              # Fluentd logging configuration
│   │   ├── apis/
│   │   │   └── user_controller.py  # REST API endpoints
│   │   ├── services/
│   │   │   ├── user.py             # Business logic layer
│   │   │   └── session.py          # Session management
│   │   ├── domain/
│   │   │   ├── entities/           # Domain entities
│   │   │   ├── enum/               # Enumerations (roles, etc.)
│   │   │   └── exception.py        # Domain exceptions
│   │   └── config/
│   │       └── config.py           # Environment configuration
│   ├── notification/               # Notification microservice
│   │   ├── main.py                 # FastAPI application
│   │   ├── models.py               # Database models
│   │   ├── consumer.py             # Kafka message consumer
│   │   ├── services/
│   │   │   ├── notification_service.py      # Core business logic
│   │   │   └── notification_adapters.py     # External integrations
│   │   ├── domain/
│   │   │   ├── entities/           # Notification entities
│   │   │   ├── ports/              # Interface definitions
│   │   │   └── enum/               # Notification types
│   │   └── config/
│   └── fluentd/
│       ├── Dockerfile              # Fluentd container setup
│       └── fluent.conf             # Log routing configuration
└── tests/                          # Test suites
    └── units/                      # Unit tests
```

## 🔧 Technologies Used

### Backend Framework

- **FastAPI**: High-performance Python web framework
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations

### Event Streaming

- **Apache Kafka**: Distributed event streaming platform
- **Confluent Kafka Python**: Python client for Apache Kafka

### Infrastructure

- **Docker & Docker Compose**: Containerization and orchestration
- **Fluentd**: Data collection and log aggregation
- **SendGrid**: Email delivery service

### Development Tools

- **Python 3.11**: Programming language
- **SQLite**: Development database
- **Uvicorn**: ASGI server for FastAPI

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Make (optional, for convenience commands)

### Quick Start

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd event_arch
   ```

2. **Set up environment variables**

   ```bash
   # Copy example environment files
   cp src/app/user/.env.example src/app/user/.env.dev
   cp src/app/notification/.env.example src/app/notification/.env.dev
   ```

3. **Run the development environment**

   ```bash
   # Using Make
   make run-dev

   # Or using Docker Compose directly
   docker compose -f docker-compose.dev.yml up --build
   ```

4. **Verify services are running**
   - User Service: http://localhost:8000/docs
   - User Service Health: http://localhost:8000/
   - Kafka: localhost:9092
   - Fluentd logs: Check Docker logs

### Environment Configuration

#### User Service (`.env.dev`)

```env
DEBUG=True
PORT=8000
DATABASE_URL=sqlite:///./test.db
HOST=localhost
```

#### Notification Service (`.env.dev`)

```env
DEBUG=True
PORT=8001
DATABASE_URL=sqlite:///./notification.db
HOST=localhost
SENDGRID_API_KEY=your_sendgrid_api_key_here
```

## 📚 API Documentation

### User Service Endpoints

#### Get All Users

```http
GET /users/
```

#### Get User by ID

```http
GET /users/{user_id}
```

#### Create User

```http
POST /users/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "role": "user",
  "age": 25,
  "full_name": "John Doe"
}
```

#### Update User

```http
PUT /users/{user_id}
Content-Type: application/json

{
  "username": "john_updated",
  "email": "john.updated@example.com"
}
```

#### Delete User

```http
DELETE /users/{user_id}
```

#### User Login

```http
POST /users/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePass123"
}
```

## 🔄 Event Flow

1. **User Creation Event**:

   ```
   User creates account → UserService.create() → Kafka 'notification' topic → NotificationService consumes event → Email sent to user
   ```

2. **Event Message Format**:
   ```json
   {
     "topic": "notification",
     "key": "user_created",
     "value": "User created with ID: 123"
   }
   ```

## 🧪 Testing

### Test Kafka Consumer

Use the provided test script to verify Kafka message flow:

```bash
python test.py
```

This will:

- Connect to Kafka on localhost:9092
- Subscribe to the 'notifications' topic
- Display all messages being published

### Manual Testing Flow

1. Start all services with `make run-dev`
2. Create a user via POST to `/users/`
3. Check Kafka messages with `python test.py`
4. Verify logs in Fluentd container

## 🐳 Docker Services

The application runs the following containers:

| Service      | Container Name   | Ports      | Description         |
| ------------ | ---------------- | ---------- | ------------------- |
| Zookeeper    | zookeeper        | 2181       | Kafka coordination  |
| Kafka        | kafka            | 9092, 9093 | Event streaming     |
| User Service | user-service-dev | 8000       | User management API |
| Fluentd      | fluentd-dev      | 24224      | Log aggregation     |

## 🔍 Monitoring & Logging

### Fluentd Configuration

- Collects logs from all services on port 24224
- Outputs structured JSON logs to stdout
- Configurable via [`fluent.conf`](src/app/fluentd/fluent.conf)

### Log Structure

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "service": "user-service",
  "action": "user_created",
  "user_id": 123,
  "details": {...}
}
```

## 🛠️ Development

### Adding New Services

1. Create service directory under `src/app/`
2. Add Dockerfile and requirements.txt
3. Update `docker-compose.dev.yml`
4. Implement Kafka consumer/producer as needed

### Adding New Event Types

1. Define event schema in producer service
2. Update Kafka topic configuration
3. Implement consumer logic in target service
4. Add appropriate error handling

## 🚀 Production Deployment

For production deployment:

1. Use `docker-compose.prod.yml` (to be configured)
2. Set up proper environment variables
3. Configure external databases (PostgreSQL recommended)
4. Set up monitoring and alerting
5. Configure proper Kafka cluster

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Author**: Ahmed  
**Architecture**: Event-Driven Microservices  
**Status**: Development
