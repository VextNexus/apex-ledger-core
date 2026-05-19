# Apex Ledger Core

A high-performance, double-entry banking ledger and fintech dashboard engineered to process secure, real-time financial transactions. The system demonstrates a robust full-stack architecture leveraging a **FastAPI** backend microservice, a persistent **PostgreSQL** database environment, and an optimized **Next.js** web client.

---

## 🏗️ Architecture & Data Consistency

### 1. Concurrency Control via SERIALIZABLE Isolation
To prevent financial anomalies such as double-spending, non-repeatable reads, and write skew under high concurrent workloads, the ledger core enforces the **Serializable Isolation Level** (the highest SQL standard) for all transactional blocks. 

### 2. Business Logic & Invariant Validation
The banking engine operates under strict transactional guarantees. Every state modification involves explicit backend invariant checking:
- **Balance Verification:** Checks if `sender.balance >= transfer_amount` within the active serializable transaction block before database commit.
- **Atomic Operations:** Ensures that a ledger transfer either succeeds completely for both nodes (Sender/Receiver) or rolls back fully, preventing partial states.
- **Fail-Safe Response:** Invalid inputs or insufficient funds trigger an immediate `400 Bad Request` safety exception, aborting database execution.

---

## 🛠️ System Tech Stack

- **Backend:** Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy ORM
- **Database:** PostgreSQL 16 (with custom connection pooling)
- **Frontend:** Next.js 14 (App Router), Tailwind CSS, TypeScript, Axios
- **Infrastructure:** Docker, Docker Compose V2

---

## 🔌 API Specification (Core Endpoints)

### 1. Account Creation
* **Endpoint:** `POST /bank/accounts`
* **Payload Type:** `application/json`
* **Request:**
```json
{
  "owner_name": "string",
  "initial_balance": 0.0000
}
```
---

## 🔐 Security & Transactional Integrity
The system implements a "fail-fast" architecture:
- **ACID Compliance:** Transactions are non-atomic only in case of explicit database constraint violations.
- **Race Condition Immunity:** By leveraging `SERIALIZABLE` isolation in PostgreSQL, the system effectively serializes concurrent transactions, preventing the "Lost Update" anomaly common in high-frequency ledgers.

## 🚀 Roadmap & Future Enhancements
- [ ] Implement JWT-based authentication for secure session management.
- [ ] Add Redis-based caching layer for high-frequency balance queries.
- [ ] Integrate real-time transaction updates via WebSockets.
- [ ] Comprehensive unit and integration testing suite using `pytest` and `Testcontainers`.

---

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
