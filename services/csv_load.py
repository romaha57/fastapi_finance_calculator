import csv
from io import StringIO
from typing import Any

from fastapi import Depends

from services.operations import OperationService
from schemas.record_schemas import RecordCreate, Record, RecordBase


class FileService:
    def __init__(self, operation_service: OperationService = Depends()):
        self.operation_service = operation_service

    def dump_csv_file(self, user_id: int, file: Any):
        reader = csv.DictReader(
            (line.decode() for line in file),
            fieldnames=["created_at", "amount", "type_operation", "description"]
        )

        records = []
        next(reader)
        for row in reader:
            record = RecordBase.parse_obj(row)
            if record.description in ('', 'string'):
                record.description = 'без описания'
            records.append(record)

        self.operation_service.create_name_records(records, user_id=user_id)

        return len(records)

    def load_csv_file(self, user_id: int):
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=["created_at", "amount", "type_operation", "description"],
            extrasaction="ignore"
        )

        writer.writeheader()
        records = self.operation_service.get_records(user_id=user_id)
        for record in records:
            data = RecordBase.from_orm(record)
            writer.writerow(data.dict())

        output.seek(0)
        return output



