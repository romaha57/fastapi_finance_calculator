import datetime

from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, ForeignKey
from sqlalchemy_utils import EmailType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(EmailType, unique=True)
    username = Column(String, unique=True)
    hash_password = Column(Text)


class RecordModel(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    amount = Column(Numeric(10, 2))
    type_operation = Column(String)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))


