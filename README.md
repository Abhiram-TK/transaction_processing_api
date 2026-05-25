# Transaction Processing API (Invoice System)

## Overview

Transaction Processing API is a backend service built using FastAPI, PostgreSQL, and SQLAlchemy.

The system supports:

- transaction creation
- transaction retrieval
- transaction updates
- pagination
- exception handling

The project exposes interactive Swagger UI documentation for live API testing.

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Uvicorn
- Python

## Architecture Overview

FastAPI Route
→ Operation Layer
→ SQLAlchemy ORM
→ PostgreSQL Database

Project Structure:

```text
transaction_processing_api/
|
├── app/
|   ├── api/
|   ├── database/
|   ├── models/
|   ├── operations/
|   └── main.py
|
├── requiremnets.txt
├── .env
└── README.md
```

## Features

- Create transaction API
- Fetch all transactions API
- Fetch single transaction API
- Update transaction API
- SQLAlchemy ORM integration
- PostgreSQL persistence
- Pagination support
- Basic exception handling
- Intercative Swagger UI

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/Abhiram-TK/transaction_processing_api
```

### 2. Navigate Into Project

```bash
cd transaction_processing_api
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

Windows:

```bash
venv\Scripts\actiavte
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Configure .env

```bash
DATABASE_URL=postgresql://postgresql://password@localhost:5432/transaction_db
```

### 7. Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

## Swagger UI

After starting the server, open:

```bash
http://127.0.0.1:8000/docs
```

Swagger UI allows:

- creating transactions
- fetching transactions
- updating transactions
- viewing API responses live

## API Endpoints

| Method | Endpoint           | Purpose                  |
| ------ | ------------------ | ------------------------ |
| POST   | /transactions      | Create transaction       |
| GET    | /transactions      | Fetch all transactions   |
| GET    | /transactions/{id} | Fecth single transaction |
| PUT    | /transaction/{id}  | Update transaction       |

## Pagination Example

GET /transaction?skip=0&limit=10

## Exception Handling

The API includes basic exception handling for:

- invalid transaction IDs
- missing transactions
- database failures

## Current Phase Status

Completed:

- FastAPI CRUD APIs
- PostgreSQL integration
- SQLAlchemy integration
- Swagger UI validation
- Pagination
- Exception handling

Next Panned Enhancements:

- JWT authentication
- Redis integration
- Rate Limiting
- Docker support
- API testing
