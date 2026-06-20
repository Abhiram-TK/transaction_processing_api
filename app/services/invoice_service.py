from datetime import datetime


def generate_invoice_number(transaction_id: int) -> str:

    current_year = datetime.utcnow().year

    return f"INV-{current_year}-{transaction_id:06d}"