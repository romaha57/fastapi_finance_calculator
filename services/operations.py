from typing import List, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db_config import create_session
from models import RecordModel
from schemas.record_schemas import OperationType, RecordCreate, RecordUpdate, Record, RecordBase


class OperationService:
    def __init__(self, session: Session = Depends(create_session)):
        self.session = session

    def _get(self, record_id: int, user_id: int) -> RecordModel:
        record = self.session.query(RecordModel).filter_by(id=record_id, user_id=user_id).first()

        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Запись с id {record_id} не найдена")
        return record

    def get_records(self, user_id: int, type_operation: Optional[OperationType] = None) -> List[RecordModel]:
        query = self.session.query(RecordModel).filter_by(user_id=user_id)
        if type_operation:
            query = query.filter_by(type_operation=type_operation)
        all_records = query.all()
        return all_records

    def get(self, record_id: int, user_id: int) -> RecordModel:
        return self._get(record_id, user_id)

    def create_name_records(self, records_data: List[RecordBase], user_id: int) -> List[RecordModel]:
        records = [RecordModel(**record.dict(),
                               user_id=user_id
                               )
                   for record in records_data]
        self.session.add_all(records)
        self.session.commit()

        return records

    def create_record(self, record_data: RecordCreate, user_id: int) -> RecordModel:
        record = RecordModel(**record_data.dict(),
                             user_id=user_id)
        self.session.add(record)
        self.session.commit()

        return record

    def update(self, record_id: int, record_data: RecordUpdate, user_id: int) -> RecordModel:
        record = self._get(record_id, user_id)
        for field, value in record_data:
            setattr(record, field, value)

        self.session.commit()
        return record

    def delete(self, record_id: int, user_id: int):
        record = self._get(record_id, user_id)
        self.session.delete(record)
        self.session.commit()
