from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class TransactionStatus(str, Enum):

    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"

class TransactionCreate(BaseModel):

    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

class TransactionUpdate(BaseModel):

    customer_name: Optional[str] = Field(None, min_length=2)
    quantity: Optional[int] = Field(None, gt=0)
    status: Optional[str] = Field(None, min_length=2)

class TransactionResponse(BaseModel):

    id: int
    customer_name: str
    product_id: int | None = None
    quantity: int | None = None
    invoice_number: str
    amount: float
    status: TransactionStatus   
    created_at: datetime
    updated_at: datetime | None = None
    validated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class TransactionMetadata(BaseModel):

    api_version: str
    processed_by: str
    timestamp: datetime

class TransactionDetailedResponse(BaseModel):

    transaction: TransactionResponse
    metadata: TransactionMetadata