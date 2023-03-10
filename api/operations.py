from typing import List, Optional

from fastapi import APIRouter, Depends

from models import UserModel
from schemas.record_schemas import (OperationType, Record, RecordCreate,
                                    RecordUpdate)
from services.auth import get_current_user
from services.operations import OperationService

operation_router = APIRouter(prefix="/operation", tags=["Record"])


@operation_router.get("/get_record_by_day")
def get_records_by_day(
    service: OperationService = Depends(),
    user: UserModel = Depends(get_current_user)
):
    """Получение записей и общей суммы трат за текущий день"""

    result, total_sum = service.get_by_time(user_id=user.id, by_day=True)
    return result, {"Общая сумма": total_sum}


@operation_router.get("/get_record_by_week")
def get_records_by_week(
    service: OperationService = Depends(),
    user: UserModel = Depends(get_current_user)
):
    """Получение записей и общей суммы трат за неделю"""

    return service.get_by_time(user_id=user.id, by_week=True)


@operation_router.get("/get_record_by_month")
def get_records_by_month(
    service: OperationService = Depends(),
    user: UserModel = Depends(get_current_user)
):
    """Получение записей и общей суммы трат за месяц"""

    return service.get_by_time(user_id=user.id, by_month=True)


@operation_router.get("/", response_model=List[Record])
def get_records(
        type_operation: Optional[OperationType] = None,
        service: OperationService = Depends(),
        user: UserModel = Depends(get_current_user)):

    """Получение всех записей из БД пользователя"""

    return service.get_records(type_operation=type_operation, user_id=user.id)


@operation_router.post("/", response_model=Record)
def create_record(
        record_data: RecordCreate,
        service: OperationService = Depends(),
        user: UserModel = Depends(get_current_user)):

    """Создание записи в БД о доходе/расходе"""

    return service.create_record(record_data, user.id)


@operation_router.get("/{record_id}")
def get_record(
        record_id: int,
        service: OperationService = Depends(),
        user: UserModel = Depends(get_current_user)):

    """Получение записи по id"""

    return service.get(record_id, user.id)


@operation_router.put("/{record_id}/update", response_model=Record)
def update_record(
        record_id: int,
        record_data: RecordUpdate,
        service: OperationService = Depends(),
        user: UserModel = Depends(get_current_user)):

    """Обновление информации о записи в БД по id"""

    return service.update(record_id, record_data, user.id)


@operation_router.delete("/{record_id}/delete")
def delete_record(
        record_id: int,
        service: OperationService = Depends(),
        user: UserModel = Depends(get_current_user)):

    """Удаление записи из БД по id"""

    service.delete(record_id, user.id)
    return {"meesage": f"Запись с id={record_id} успешно удалена"}
