from fastapi import APIRouter

from app.operations.transaction_ops import (create_transaction, get_all_transactions, get_transaction_by_id, update_transactions)

router = APIRouter()

@router.post("/transactions")
def create_transaction_route(customer_name: str, invoice_number: str, amount: float, status: str):

    transaction = create_transaction(customer_name, invoice_number, amount, status)

    return transaction

@router.get("/transactions")
def fetch_all_transactions():

    transactions = get_all_transactions()

    return transactions

@router.get("/transactions/{transaction_id}")
def fetch_transaction(transaction_id: int):

    transaction = get_transaction_by_id(transaction_id)

    return transaction

@router.put("/transactions/{transaction_id}")
def update_transaction_route(transcation_id: int, customer_name: str, amount: float, status: str):

    transaction = update_transactions(transcation_id, customer_name, amount, status)

    return transaction





