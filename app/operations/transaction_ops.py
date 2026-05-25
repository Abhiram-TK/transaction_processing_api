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

