from sqlalchemy.orm import Session

from app.models.transaction import Transaction

def create_transaction(db: Session, customer_name, invoice_number, amount):

    new_transaction = Transaction(customer_name=customer_name, invoice_number=invoice_number, amount=amount, status="PENDING")

    db.add(new_transaction)

    db.commit()

    db.refresh(new_transaction)

    from app.workers.transaction_tasks import (validate_transaction)

    validate_transaction.delay(new_transaction.id)

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

    db.commit()

    db.refresh(transaction)

    return transaction