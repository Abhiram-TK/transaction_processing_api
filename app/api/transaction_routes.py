from fastapi import APIRouter

from app.operations.transaction_ops import create_transaction

router = APIRouter()

@router.post("/transactions")
def create_transaction_route(customer_name: str, invoice_number: str, amount: float, status: str):

    transaction = create_transaction(customer_name, invoice_number, amount, status)

    return transaction

