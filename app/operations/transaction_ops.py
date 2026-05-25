from app.database.connection import SessionLocal

from app.models.transaction import Transaction

def create_transaction(customer_name, invoice_number, amount, status):

    db = SessionLocal()

    new_transaction = Transaction(customer_name=customer_name, invoice_number=invoice_number, amount=amount, status=status)

    db.add(new_transaction)

    db.commit()

    db.refresh(new_transaction)

    db.close()

    return new_transaction

def get_all_transactions():

    db = SessionLocal()

    transactions = db.query(Transaction).all()

    db.close()

    return transactions

def get_transaction_by_id(transaction_id):

    db = SessionLocal()

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    db.close()

    return transaction

def update_transactions(transaction_id, customer_name, amount, status):

    db = SessionLocal()

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:

        db.close()

        return None
    
    if amount <= 0:

        db.close()

        return None
    
    transaction.customer_name = customer_name

    transaction.amount = amount

    transaction.status = status

    db.commit()

    db.refresh(transaction)

    db.close()

    return transaction



