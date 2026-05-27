from pydantic import BaseModel, Field
from typing import Optional

class TransactionCreate(BaseModel):

    customer_name: str = Field(..., min_length=2)

    invoice_number: str = Field(..., min_length=3)

    amount: float = Field(..., gtr=0)

    status: str = Field(..., min_length=2)

class TransactionUpdate(BaseModel):

    customer_name: Optional[str] = Field(None, min_length=2)

    invoice_number: Optional[str] = Field(None, min_length=3)

    amount: Optional[float] = Field(None, gt=0)

    status: Optional[str] = Field(None, min_length=2)

