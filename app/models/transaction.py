from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import DateTime
from sqlalchemy import CheckConstraint

from datetime import datetime

from app.database.connection import Base

class Transaction(Base):

    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String, nullable=False)

    invoice_number = Column(String, unique=True, nullable=False)

    amount = Column(Numeric, nullable=False)

    status = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (CheckConstraint("amount > 0", name="check_amount_positive"),)

    