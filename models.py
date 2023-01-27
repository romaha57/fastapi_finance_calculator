import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, Numeric, String,
                        Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import EmailType

Base = declarative_base()


class UserModel(Base):
    """Модель для пользователя"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(EmailType, unique=True)
    username = Column(String, unique=True)
    hash_password = Column(Text)


class RecordModel(Base):
    """Модель для записи(учет доходов/расходов)"""

    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    amount = Column(Numeric(10, 2))
    type_operation = Column(String)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
