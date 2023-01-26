from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends

from models import UserModel
from schemas.record_schemas import Record, OperationType, RecordCreate, RecordUpdate
from services.auth import get_current_user
from services.operations import OperationService


operation_router = APIRouter(prefix="/operation", tags=["Record"])


@operation_router.get("/", response_model=List[Record])
def get_records(
        type_operation: Optional[OperationType] = None,
        service: OperationService = Depends(),
        user: UserModel = Depends(get_current_user)):

    return service.get_records(type_operation, user.id)


@operation_router.post("/", response_model=Record)
def create_record(
        record_data: RecordCreate,
        service: OperationService = Depends(),
    user: UserModel = Depends(get_current_user)):

    return service.create_record(record_data, user.id)


@operation_router.get("/{record_id}")
def get_record(
        record_id: int,
        service: OperationService = Depends(),
        user: UserModel = Depends(get_current_user)):

    return service.get(record_id, user.id)


@operation_router.put("/{record_id}/update", response_model=Record)
def update_record(
        record_id: int,
        record_data: RecordUpdate,
        service: OperationService = Depends(),
        user: UserModel = Depends(get_current_user)):

    return service.update(record_id, record_data, user.id)


@operation_router.delete("/{record_id}/delete")
def delete_record(
        record_id: int,
        service: OperationService = Depends(),
        user: UserModel = Depends(get_current_user)):

    service.delete(record_id, user.id)
    return {"meesage": f"Запись с id={record_id} успешно удалена"}