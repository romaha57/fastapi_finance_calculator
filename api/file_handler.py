from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks

from models import UserModel
from services.auth import get_current_user
from services.csv_load import FileService
from fastapi.responses import StreamingResponse

file_router = APIRouter(prefix="/file", tags=["CSV-report"])



@file_router.post("/dump")
def dump_csv(
        back_tasks: BackgroundTasks,
        user: UserModel = Depends(get_current_user),
        file: UploadFile = File(...),
        service: FileService = Depends()):

    back_tasks.add_task(service.dump_csv_file,
                        user.id,
                        file.file)

    return {"message": f"Успешно добавлено записи"}


@file_router.get("/load")
def load_csv(user: UserModel = Depends(get_current_user),
             service: FileService = Depends()):

    records = service.load_csv_file(user_id=user.id)
    return StreamingResponse(
        records,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=report.csv"}
    )