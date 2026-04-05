# Finance Data Processing & Access Control Backend

A **production-ready REST API** built with **FastAPI** to manage financial records with strong emphasis on:

* Security
* Data Integrity
* Scalability

Developed as part of the **Zorvyn Backend Developer Internship Assignment**.

---

## Key Features

### Authentication & Authorization

* OAuth2-based authentication with **JWT tokens**
* Secure password hashing using **bcrypt**
* Role-Based Access Control (**RBAC**):

  * `Admin`
  * `Analyst`
  * `Viewer`
* Support for **active/inactive users**

---

### Financial Records Management

* Full **CRUD operations**
* **Soft Delete** (`is_deleted` flag) for audit safety
* Strict validation using **Pydantic + Enums**
* Advanced querying:

  * Pagination (`skip`, `limit`)
  * Filtering (`category`, `type`)
  * Case-insensitive search

---

### Dashboard & Analytics

* Real-time financial summaries:

  * Total Income
  * Total Expense
  * Net Balance
* Category-wise breakdown using SQL `GROUP BY`

---

## Tech Stack

| Layer        | Technology   |
| ------------ | ------------ |
| Framework    | FastAPI      |
| Database     | SQLite       |
| ORM          | SQLAlchemy   |
| Validation   | Pydantic v2  |
| Auth         | OAuth2 + JWT |
| Package Mgmt | uv           |

---

## Project Structure

```text
finance-dashboard-backend/
│
├── app/
│   ├── main.py          # Entry point & route registration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Business logic
│   ├── auth.py          # Authentication & RBAC
│   └── database.py      # DB setup
│
├── .env                 # Environment variables
├── pyproject.toml       # Dependencies (uv)
└── finance.db           # SQLite DB (auto-generated)
```

---

## Quick Start

### 1. Prerequisites

Ensure **uv** is installed:

```bash
pip install uv
```

### 2. Installation

```bash
git clone https://github.com/your-username/your-repo-name.git
cd finance-dashboard-backend
uv sync
```
---

### 3. .env File Creation

Create a .env file in the root directory like following example:

```bash 
SECRET_KEY="your-extremely-safe-and-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
Note: The SECRET_KEY is used to sign JWT tokens. Ensure this is kept private.

---

### 3. Run the Server

```bash
uv run uvicorn app.main:app --reload
```

---

### 4. API Docs (Swagger UI)

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Interactive API testing directly in browser.

---

## API Endpoints

### Authentication

| Endpoint  | Method | Access | Description   |
| --------- | ------ | ------ | ------------- |
| `/signup` | POST   | Public | Register user |
| `/login`  | POST   | Public | Get JWT token |

---

### Financial Records

| Endpoint        | Method | Access          | Description                       |
| --------------- | ------ | --------------- | --------------------------------- |
| `/records/`     | GET    | Authenticated   | Fetch records (filters supported) |
| `/records/`     | POST   | Admin / Analyst | Create record                     |
| `/records/{id}` | PUT    | Admin / Analyst | Update record                     |
| `/records/{id}` | DELETE | Admin           | Soft delete                       |

---

### Dashboard

| Endpoint             | Method | Access        | Description       |
| -------------------- | ------ | ------------- | ----------------- |
| `/dashboard/my-summary` | GET    | Authenticated | Financial summary of indvidual|
| `/dashboard/company-summary` | GET    | Authenticated | Financial summary of company|

---

## Testing via Swagger

1. Start server → `/docs`
2. Create user via `/signup`
3. Login → get `access_token`
4. Click **Authorize**
5. Paste token
6. Test protected endpoints

---

## Technical Decisions

### Why FastAPI?

* Async support → high performance
* Built-in Swagger docs
* Tight integration with Pydantic

---

### Database & ORM

* **SQLite** → zero setup, portable
* **SQLAlchemy** → scalable abstraction (easy PostgreSQL migration)

---

### Enum-Driven Design

Strict enums ensure:

* No invalid categories
* Clean analytics
* Predictable data

---

### Security

* JWT → stateless, scalable auth
* bcrypt → secure password storage
* Dependency-based RBAC → clean architecture

---

### Engineering Practices

* Soft delete → audit trail
* Pagination → scalable queries
* Case-insensitive search → better UX

---

## Data Dictionary

### Roles

| Role      | Permissions            |
| --------- | ---------------------- |
| `admin`   | Full access(create,read,update,delete) | 
| `analyst` | Create + Update + Read but not delete|
| `viewer`  | Read-only              |

---

### Record Types

* `income`
* `expense`

---

### Categories

* `salary`
* `food`
* `rent`
* `utilities`
* `entertainment`
* `transport`
* `other`

---

##  Assumptions & Constraints

* Fixed categories ensure **clean analytics**
* Role permissions strictly enforced
* Soft delete preserves historical data

---

## Allowed Values (Enums)
### IMPORTANT:
When testing the API, you must use the following case-sensitive values, otherwise the API will return a 422 Validation Error.

Roles: admin, analyst, viewer

Types: income, expense

Categories: salary, food, rent, utilities, entertainment, transport, other