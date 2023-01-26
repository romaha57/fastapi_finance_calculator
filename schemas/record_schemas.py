from datetime import datetime
from typing import Optional
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class OperationType(str, Enum):
    income = "income"
    outcome = "expenses"


class RecordBase(BaseModel):
    created_at: datetime = datetime.now()
    amount: Decimal
    type_operation: OperationType
    description: Optional[str]

    class Config:
        orm_mode = True


class Record(RecordBase):
    id: int

    class Config:
        orm_mode = True


class RecordCreate(RecordBase):
    pass


class RecordUpdate(RecordBase):
    pass
