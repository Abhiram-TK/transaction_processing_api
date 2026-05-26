import time

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.events.event_emitter import emit_event

from fastapi import (APIRouter, HTTPException, Request, Response, status, Depends, Header)

from app.operations.transaction_ops import (create_transaction, get_all_transactions, get_transaction_by_id, update_transactions)

processed_requests = {}

request_tracker = {}

RATE_LIMIT = 5
TIME_WINDOW = 60

router = APIRouter()

@router.post("/transactions",status_code=status.HTTP_201_CREATED)
def create_transaction_route(request: Request, response: Response, customer_name: str, invoice_number: str, amount: float, status: str, idempotency_key: str = Header(...), 
                             db: Session = Depends(get_db)):
    
    client_ip = request.client.host

    current_time = time.time()

    if client_ip not in request_tracker:

        request_tracker[client_ip] = []

    recent_requests = []

    for timestamp in request_tracker[client_ip]:

        if current_time - timestamp < TIME_WINDOW:

            recent_requests.append(timestamp)

    request_tracker[client_ip] = recent_requests

    if len(request_tracker[client_ip]) >= RATE_LIMIT:

        raise HTTPException(status_code=429, detail="Rate limit exceeded", headers={"X-RateLimit-Limit": str(RATE_LIMIT), "X-RateLimit-Remaining": "0"})
    
    request_tracker[client_ip].append(current_time)

    remaining_requests = RATE_LIMIT - len(request_tracker[client_ip])

    response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)

    response.headers["X-RateLimit-Remaining"] = str(max(remaining_requests, 0))

    if idempotency_key in processed_requests:

        return processed_requests[idempotency_key]

    try:

        transaction = create_transaction(db, customer_name, invoice_number, amount, status)

        emit_event(event_name="TRANSACTION_CREATED", payload={"transaction_id": transaction.id, "invoice_number": transaction.invoice_number, "amount": transaction.amount})

        processed_requests[idempotency_key] = transaction

        return transaction
    
    except Exception:

        raise HTTPException(status_code=500, detail="Database operation failed")

@router.get("/transactions")
def fetch_all_transactions(response: Response, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    response.headers["X-API-Version"] = "1.0"

    transactions = get_all_transactions(db, skip, limit)

    return transactions

@router.get("/transactions/{transaction_id}")
def fetch_transaction(transaction_id: int, db: Session = Depends(get_db)):

    transaction = get_transaction_by_id(db, transaction_id)

    if not transaction:

        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

@router.put("/transactions/{transaction_id}")
def update_transaction_route(transaction_id: int, customer_name: str, amount: float, status: str, db: Session = Depends(get_db)):

    transaction = update_transactions(db, transaction_id, customer_name, amount, status)

    if not transaction: 

        raise HTTPException(status_code=400, detail="Invalid transaction update")

    return transaction





