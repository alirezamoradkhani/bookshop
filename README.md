# 📚 Bookshop API

A production-grade, event-driven backend system for a digital bookshop platform built with **FastAPI**, designed using **Clean Architecture**, **async-first execution**, and **distributed event-driven architecture**.

This project demonstrates a modular monolith evolving toward a scalable distributed system using messaging, outbox patterns, and CQRS-style read models.

# 🚀 Architecture at a Glance

The system is built around **event-driven consistency** and **async processing pipelines**:

Client  
↓  
FastAPI (API Layer)  
↓  
PostgreSQL (Source of Truth)  
↓  
Outbox Table (Transactional Events)  
↓  
Outbox Worker  
↓  
RabbitMQ (Event Bus)  
↓  
Consumers  
- Order Processing  
- Payment Handling  
- Analytics Pipeline  
- Borrowing Workflow  
- Meilisearch Indexer  

# ✨ Core Features

## 📖 Business Features
- Book catalog browsing
- Purchase & order processing
- Borrowing system (due dates, waitlists, overdue handling)
- Author & edition management
- Transaction tracking & auditability

## ⚙️ System Features
- Fully async FastAPI backend
- Event-driven architecture (RabbitMQ)
- Reliable event delivery (Outbox Pattern)
- CQRS-style search layer (Meilisearch)
- Redis caching (OTP, idempotency, rate limiting)
- Background workers for async workflows

# 🧠 Architecture Principles

## 🧩 Modular Monolith
- user → authentication & identity  
- book → catalog domain  
- order → purchase flow  
- borrow → borrowing logic  
- transaction → financial records  
- analytics → metrics pipeline  
- search → Meilisearch read model  

## 🔁 Event-Driven Consistency

1. Domain action occurs (e.g. order created)  
2. Transaction commits in PostgreSQL  
3. Event stored in outbox table  
4. Worker publishes event to RabbitMQ  
5. Consumers react asynchronously  

## 🔎 Search (CQRS Read Model)

Meilisearch is used as a dedicated read model:

Domain Event → Outbox → Worker → Meilisearch → Search API  

Features:
- Full-text search
- Typo tolerance
- Filtering (price, category, availability)
- Near real-time indexing

# 🛠 Tech Stack

- FastAPI
- PostgreSQL 16
- SQLAlchemy (async)
- Redis 7
- RabbitMQ
- Meilisearch
- APScheduler
- JWT (python-jose)
- SlowAPI

# 📦 Project Structure

app/
- api/                    HTTP routes
- core/                   config & settings
- database.py            DB session
- user/                  auth & identity
- book/                  catalog domain
- edition/               book editions
- order/                 order processing
- borrow/                borrowing system
- transaction/           payments
- analytics/             metrics
- search/                Meilisearch integration
- broker/                Redis + RabbitMQ adapters
- workers/               background workers
- outbox/                event publishing
- exceptions/           domain errors
- dependency_injection/  DI container

# ⚙️ Getting Started

## 1. Clone repository
git clone https://github.com/<your-org>/bookshop.git  
cd bookshop  

## 2. Environment setup
cp .env.example .env  

Required variables:
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/bookshop  
REDIS_URL=redis://redis:6379/0  
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/  
MEILI_URL=http://meilisearch:7700  
MEILI_MASTER_KEY=secret  
JWT_SECRET=super-secret  
DEBUG=true  

## 3. Run with Docker
docker compose up --build -d  

Includes:
- FastAPI
- PostgreSQL
- Redis
- RabbitMQ
- Meilisearch
- Workers

## 4. Migrations
alembic upgrade head  

## 5. API
http://localhost:8000  
/docs  
/redoc  

# 🧵 Workers

- Outbox Worker → publish events  
- Consumer Workers → process domain events  
- Scheduler Worker → periodic tasks  

Goals:
- idempotent processing
- retry safety
- isolation of failures

# 🔐 Security

- JWT authentication
- Password hashing
- OTP via Redis
- Rate limiting
- Idempotency keys

# 🔎 Search System (Meilisearch)

- Full-text search
- Typo tolerance
- Fast filtering
- Near real-time indexing (<1s)

# 📈 Highlights

- Event-driven architecture
- Outbox pattern reliability
- CQRS-style read model
- Async-first design
- Modular monolith structure

# 🚀 Future Improvements

- Payment gateway integration
- OpenTelemetry tracing
- Prometheus + Grafana
- Kafka migration
- Recommendation system
- Advanced search ranking

# 🤝 Contribution

- Fork repo
- Create branch
- Follow conventional commits
- Add tests
- Submit PR

# 📄 License

MIT or project-defined license

# 🧠 Final Note

Designed as a real-world backend system focused on:
- reliability
- scalability
- clean architecture
- event-driven consistency