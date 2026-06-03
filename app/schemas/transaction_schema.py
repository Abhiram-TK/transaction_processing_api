from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class TransactionCreate(BaseModel):

    customer_name: str = Field(..., min_length=2)
    invoice_number: str = Field(..., min_length=3)
    amount: float = Field(..., gt=0)

class TransactionUpdate(BaseModel):

    customer_name: Optional[str] = Field(None, min_length=2)
    invoice_number: Optional[str] = Field(None, min_length=3)
    amount: Optional[float] = Field(None, gt=0)
    status: Optional[str] = Field(None, min_length=2)

class TransactionResponse(BaseModel):

    id: int
    customer_name: str
    invoice_number: str
    amount: float
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TransactionMetadata(BaseModel):

    api_version: str
    processed_by: str
    timestamp: datetime

class TransactionDetailedResponse(BaseModel):

    transaction: TransactionResponse
    metadata: TransactionMetadata