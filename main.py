import uvicorn
from fastapi import FastAPI

from api.auth import auth_router
from api.file_handler import file_router
from api.operations import operation_router
from db_config import engine
from models import Base
from config import settings

tags_metadata = [
    {
        "name": "Users",
        "description": "Регистрация и аутентификация пользователя"
    },
    {
        "name": "CSV-report",
        "description": "Создание отчета и выгрузка в БД"
    },    {
        "name": "Record",
        "description": "CRUD-операции с записями о доходах и расходах"
    }
]

app = FastAPI(
    title="Personal Finance Calculator ",
    description="Сервис по учету личных доходов и расходов",
    version="0.1",
    openapi_tags=tags_metadata
)
app.include_router(auth_router)
app.include_router(operation_router)
app.include_router(file_router)


if __name__ == "__main__":
    # создаем БД
    Base.metadata.create_all(engine)
    uvicorn.run("main:app", host="0.0.0.0", port=settings.server_port, reload=True)
