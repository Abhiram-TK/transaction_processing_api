from sqlalchemy import Column, Integer, String, Numeric, DateTime, CheckConstraint, Enum

from datetime import datetime

from app.database.connection import Base

import enum

class TransactionStatus(enum.Enum):

    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"

class Transaction(Base):

    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String, nullable=False)

    product_id = Column(Integer, nullable=True)

    quantity = Column(Integer, nullable=True)

    invoice_number = Column(String, unique=True, nullable=False)

    amount = Column(Numeric, nullable=False)

    status = Column(Enum(TransactionStatus), nullable=False, default=TransactionStatus.PENDING)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (CheckConstraint("amount > 0", name="check_amount_positive"),) 