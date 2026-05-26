from fastapi import APIRouter, Response, Header
from fastapi import Depends
from fastapi import HTTPException, status

from app.operations.transaction_ops import (create_transaction, get_all_transactions, get_transaction_by_id, update_transactions)

from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

processed_requests = {}

router = APIRouter()

@router.post("/transactions",status_code=status.HTTP_201_CREATED)
def create_transaction_route(customer_name: str, invoice_number: str, amount: float, status: str, idempotency_key: str = Header(...), db: Session = Depends(get_db)):

    if idempotency_key in processed_requests:

        return processed_requests[idempotency_key]

    try:

        transaction = create_transaction(db, customer_name, invoice_number, amount, status)

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





