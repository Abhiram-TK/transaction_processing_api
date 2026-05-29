import time
from datetime import datetime

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.events.event_emitter import emit_event
from app.operations.transaction_ops import (create_transaction, get_all_transactions, get_transaction_by_id, update_transactions)
from app.schemas.transaction_schema import (TransactionCreate, TransactionUpdate, TransactionResponse, TransactionMetadata, TransactionDetailedResponse)
from app.middleware.auth_middleware import get_current_user
from app.services.rbac_service import RoleChecker

from fastapi import (APIRouter, HTTPException, Request, Response, status, Depends, Header)

from app.core.logger import logger


processed_requests = {}

request_tracker = {}

RATE_LIMIT = 5
TIME_WINDOW = 60

router = APIRouter()

@router.post("/transactions",status_code=status.HTTP_201_CREATED, response_model=TransactionResponse, dependencies=[Depends(RoleChecker(["admin", "recruiter"]))])

def create_transaction_route(request: Request, response: Response, transaction: TransactionCreate, idempotency_key: str = Header(...), 
                             db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
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

        transaction = create_transaction(db, transaction.customer_name, transaction.invoice_number, transaction.amount, transaction.status)

        emit_event(event_name="TRANSACTION_CREATED", payload={"transaction_id": transaction.id, "invoice_number": transaction.invoice_number, "amount": transaction.amount})

        processed_requests[idempotency_key] = transaction

        return transaction
    
    except Exception as e:

        logger.error(f"Transaction creation failed: {str(e)}")

        raise HTTPException(status_code=500, detail="Database operation failed")
        

@router.get("/transactions", response_model=list[TransactionResponse], dependencies=[Depends(RoleChecker(["admin", "recruiter", "viewer"]))])

def fetch_all_transactions(response: Response, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    response.headers["X-API-Version"] = "1.0"

    transactions = get_all_transactions(db, skip, limit)

    return transactions

@router.get("/transactions/{transaction_id}", response_model=TransactionDetailedResponse, dependencies=[Depends(RoleChecker(["admin", "recruiter", "viewer"]))])

def fetch_transaction(transaction_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    transaction = get_transaction_by_id(db, transaction_id)

    if not transaction:

        raise HTTPException(status_code=404, detail="Transaction not found")

    return {"transaction": transaction, "metadata": {"api_version": "1.0", "processed_by": "FastAPI Transaction Service", "timestamp": datetime.utcnow()}}

@router.put("/transactions/{transaction_id}", response_model=TransactionResponse, dependencies=[Depends(RoleChecker(["admin"]))])

def update_transaction_route(transaction_id: int, transaction_update: TransactionUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    transaction = update_transactions(db, transaction_id, transaction_update.customer_name, transaction_update.amount, transaction_update.status)

    if not transaction: 

        raise HTTPException(status_code=400, detail="Invalid transaction update")

    return transaction





