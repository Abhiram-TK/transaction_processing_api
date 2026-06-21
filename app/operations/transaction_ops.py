from datetime import datetime

from sqlalchemy.orm import Session

from app.models.transaction import Transaction

from app.services.invoice_service import generate_invoice_number
from app.services.product_service import fetch_product_by_id

def create_transaction(db: Session, customer_name, product_id, quantity, token):

    product = fetch_product_by_id(product_id=product_id, token=token)

    if not product:

        raise Exception("Product not found")
    
    amount = product["price"] * quantity

    new_transaction = Transaction(customer_name=customer_name, product_id=product_id, quantity=quantity, invoice_number="TEMP", amount=amount, status="PENDING")

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    new_transaction.invoice_number = generate_invoice_number(new_transaction.id)

    db.commit()
    db.refresh(new_transaction)

    return new_transaction

def get_all_transactions(db: Session, skip: int = 0, limit: int = 10):

    transactions = db.query(Transaction)\
        .offset(skip)\
            .limit(limit)\
                .all()

    return transactions

def get_transaction_by_id(db: Session, transaction_id):

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    return transaction

def update_transactions(db: Session, transaction_id, customer_name, amount, status):

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:

        return None
    
    if amount <= 0:

        return None
    
    transaction.customer_name = customer_name

    transaction.amount = amount

    transaction.status = status

    transaction.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(transaction)

    return transaction