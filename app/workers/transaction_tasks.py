from datetime import datetime

from app.workers.celery_app import celery_app

from app.database.connection import SessionLocal

from app.models.transaction import Transaction

@celery_app.task
def validate_transaction(transaction_id):

    db = SessionLocal()

    try:

        transaction = (db.query(Transaction).filter(Transaction.id == transaction_id).first())

        if not transaction:
            return

        validation_passed = True

        if transaction.amount <= 0:

            validation_passed = False

        if not transaction.invoice_number:

            validation_passed = False

        if not transaction.customer_name:

            validation_passed = False

        duplicate_count = (db.query(Transaction).filter(Transaction.invoice_number == transaction.invoice_number).count())

        if duplicate_count > 1:

            validation_passed = False

        if validation_passed:

            transaction.status = "VALIDATED"

            transaction.validated_at = datetime.utcnow()

        else:

            transaction.status = "FAILED"

            transaction.updated_at = datetime.utcnow()

        db.commit()

    except Exception as error:

        print(error)

    finally:

        db.close()