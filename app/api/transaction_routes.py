from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.operations.transaction_ops import (create_transaction, get_all_transactions, get_transaction_by_id, update_transactions)

from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

router = APIRouter()

@router.post("/transactions")
def create_transaction_route(customer_name: str, invoice_number: str, amount: float, status: str, db: Session = Depends(get_db)):

    try:

        transaction = create_transaction(db, customer_name, invoice_number, amount, status)

        return transaction
    
    except Exception:

        raise HTTPException(status_code=500, detail="Database operation failed")

@router.get("/transactions")
def fetch_all_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    transactions = get_all_transactions(db, skip, limit)

    return transactions

@router.get("/transactions/{transaction_id}")
def fetch_transaction(transaction_id: int, db: Session = Depends(get_db)):

    transaction = get_transaction_by_id(db, transaction_id)

    if not transaction:

        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

@router.put("/transactions/{transaction_id}")
def update_transaction_route(transcation_id: int, customer_name: str, amount: float, status: str, db: Session = Depends(get_db)):

    transaction = update_transactions(db, transcation_id, customer_name, amount, status)

    if not transaction: 

        raise HTTPException(status_code=400, detail="Invalid transaction update")

    return transaction





