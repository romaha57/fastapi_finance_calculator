from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class OperationType(str, Enum):
    """Тип операции доход/расход"""

    income = "income"
    outcome = "expenses"


class RecordBase(BaseModel):
    """Базовая модель записи"""

    created_at: datetime = datetime.now()
    amount: Decimal
    type_operation: OperationType
    description: Optional[str]

    class Config:
        orm_mode = True


class Record(RecordBase):
    """Модель записи для отображения"""

    id: int

    class Config:
        orm_mode = True


class RecordCreate(RecordBase):
    """Модель записи для создания"""

    pass


class RecordUpdate(RecordBase):
    """Модель записи для обновления"""

    pass
