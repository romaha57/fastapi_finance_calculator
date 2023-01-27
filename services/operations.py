import datetime
from typing import List, Optional, Tuple

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db_config import create_session
from models import RecordModel
from schemas.record_schemas import (OperationType, RecordBase,
                                    RecordCreate, RecordUpdate)


class OperationService:
    """Класс операции над записями в БД"""

    def __init__(self, session: Session = Depends(create_session)) -> None:
        """Инициализации сессии для работы с БД"""

        self.session = session

    def _get(self, record_id: int, user_id: int) -> RecordModel:
        """Получение записи по id"""

        record = self.session.query(RecordModel).filter_by(id=record_id, user_id=user_id).first()

        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Запись с id {record_id} не найдена")
        return record

    def _get_records_by_user(self, user_id: int) -> List[RecordModel]:
        """Получение всех записей для пользоваля по его id"""

        query = self.session.query(RecordModel).filter_by(user_id=user_id).all()

        return query

    def _calculate_sum(self, record: RecordModel) -> int:
        """Считает сумму трат/доходов за определенный период"""

        if record.type_operation == 'income':
            self.total_sum += record.amount
        elif record.type_operation == 'expenses':
            self.total_sum -= record.amount

        return self.total_sum

    def _get_by_time(self,
                     user_id: int, by_day: Optional,
                     by_week: Optional, by_month: Optional) -> List[RecordModel]:

        """Получение записей из БД за определенный промежутое времени,
        исходя из флага by_day/by_week/by_month"""

        result = []
        self.total_sum = 0
        now = datetime.datetime.now().date()
        records = self._get_records_by_user(user_id)

        for record in records:
            if by_day:
                if record.created_at.date() == now:
                    result.append(record)
                    self._calculate_sum(record)
            elif by_week:
                if now - datetime.timedelta(days=7) <= record.created_at.date() <= now:
                    result.append(record)
                    self._calculate_sum(record)

            elif by_month:
                if now - datetime.timedelta(days=30) <= record.created_at.date() <= now:
                    result.append(record)
                    self._calculate_sum(record)

        return result

    def get_records(self,
                    user_id: int,
                    type_operation: Optional[OperationType] = None) -> List[RecordModel]:

        """Получение всех записей и фильтр их по полю 'type_opearion'"""

        query = self.session.query(RecordModel).filter_by(user_id=user_id)
        if type_operation:
            query = query.filter_by(type_operation=type_operation)
        all_records = query.all()

        return all_records

    def get(self, record_id: int, user_id: int) -> RecordModel:
        """Получение записей пользователя"""

        return self._get(record_id, user_id)

    def get_by_time(self,
                    user_id: int,
                    by_day: Optional = None,
                    by_week: Optional = None,
                    by_month: Optional = None) -> Tuple[List[RecordModel], int]:

        """Получение записей из БД за определенный промежутое времени,
        исходя из флага by_day/by_week/by_month"""

        result = self._get_by_time(user_id, by_day, by_week, by_month)

        return result, self.total_sum

    def create_many_records(self,
                            records_data: List[RecordBase],
                            user_id: int) -> List[RecordModel]:

        """Создает несколько записей об операции дохода/расхода в БД"""

        records = [RecordModel(**record.dict(),
                               user_id=user_id
                               )
                   for record in records_data]
        self.session.add_all(records)
        self.session.commit()

        return records

    def create_record(self, record_data: RecordCreate, user_id: int) -> RecordModel:

        """Создает запись об операции дохода/расхода в БД"""

        record = RecordModel(**record_data.dict(),
                             user_id=user_id)
        self.session.add(record)
        self.session.commit()

        return record

    def update(self, record_id: int, record_data: RecordUpdate, user_id: int) -> RecordModel:

        """Обновление данных о записи"""

        record = self._get(record_id, user_id)
        for field, value in record_data:
            setattr(record, field, value)

        self.session.commit()
        return record

    def delete(self, record_id: int, user_id: int) -> None:

        """Удаление записи"""

        record = self._get(record_id, user_id)
        self.session.delete(record)
        self.session.commit()
