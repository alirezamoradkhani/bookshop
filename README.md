# 📚 Bookshop API

A scalable, event-driven backend system for a bookshop platform built with **FastAPI**, designed using clean architecture principles, async processing, and distributed messaging.

---

## 🧭 Overview

This project implements a backend system for managing a digital bookshop platform where users can:

- Browse and purchase books
- Borrow books for a limited period
- Authors can publish books and editions
- Admins manage the platform ecosystem

The system is designed to handle **high concurrency, async workflows, and reliable event processing** using a combination of PostgreSQL, Redis, and RabbitMQ.

---

## 🏗 Architecture

The system is built using a **modular monolithic architecture with event-driven capabilities**.

### Key Design Principles:

- Separation of domain modules (Users, Books, Orders, etc.)
- Async-first design using FastAPI + async SQLAlchemy
- Event-driven communication via RabbitMQ
- Outbox pattern for reliable event delivery
- External integrations abstracted via broker layer
- Redis used for:
  - OTP verification
  - Idempotency control
  - Temporary caching

---

## 🔁 Event Flow (Simplified)

Typical flow example:

1. User creates an order
2. Order is stored in PostgreSQL
3. Event is written to Outbox table
4. Background worker picks event
5. Event is published to RabbitMQ
6. Consumers process:
   - Payment
   - Inventory update
   - Analytics tracking

---

## 🧰 Tech Stack

- **FastAPI** – API framework
- **PostgreSQL** – Primary database
- **Redis** – Cache, OTP, idempotency
- **RabbitMQ** – Event broker
- **SQLAlchemy (async)** – ORM
- **Alembic** – Database migrations
- **JWT** – Authentication
- **Docker & Docker Compose** – Deployment

---

## 👥 Domain Modules

- 👤 `user` – Authentication & user management
- 📚 `book` – Book catalog management
- 📖 `edition` – Book versions/editions
- 🛒 `order` – Purchase system
- 💳 `transaction` – Payment tracking
- 📥 `borrow` – Borrowing system
- 📊 `analytics` – Usage insights & metrics

---

## 📡 Background System

The project includes a dedicated worker system for:

- Outbox event delivery
- Scheduled tasks
- Async message processing (RabbitMQ consumers)

This ensures **eventual consistency and reliability** across the system.

---

## 🔐 Security Model

- JWT-based authentication
- Password hashing (secure storage)
- OTP verification via Redis
- Idempotent request handling for critical operations

---

## 📁 Project Structure

```text
app/
│
├── api/              # API routes
├── user/             # User domain
├── book/             # Book domain
├── edition/          # Book editions
├── order/            # Orders
├── borrow/           # Borrow system
├── transaction/      # Payments
├── analytics/        # Metrics
│
├── broker/           # Redis & RabbitMQ integration
├── workers/          # Background workers
├── exceptions/       # Custom errors
├── core/             # Settings & config
├── database.py       # DB session