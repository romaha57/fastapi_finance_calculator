import datetime

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from db_config import create_session
from schemas.auth_schemas import User, Token, UserCreate
from models import UserModel

from config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


def get_current_user(token: str = Depends(oauth2_scheme)):
    return AuthService.validate_token(token)


class AuthService:

    @classmethod
    def hash_password(cls, raw_password: str) -> str:
        return bcrypt.hash(raw_password)

    @classmethod
    def verify_password(cls, password: str, hash_password: str) -> bool:
        return bcrypt.verify(password, hash_password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный токен",
                headers={"WWW-Authenticate": "Bearer"}
            )

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
        except jwt.JWTError:
            raise exception

        user_data = payload.get("user")
        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception

        return user

    @classmethod
    def create_token(cls, user: UserModel) -> Token:
        user_data = User.from_orm(user)

        now = datetime.datetime.utcnow()

        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + datetime.timedelta(seconds=settings.jwt_expiration),
            "sub": str(user_data.id),
            "user": user_data.dict()
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret,
            settings.jwt_algorithm
        )

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(create_session)):
        self.session = session

    def registration_user(self, user: UserCreate) -> Token:
        user = UserModel(
            email=user.email,
            username=user.username,
            hash_password=self.hash_password(user.password)
        )

        self.session.add(user)
        self.session.commit()

        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )

        user = self.session.query(UserModel).filter_by(username=username).first()

        if not user:
            raise exception

        if not self.verify_password(password, user.hash_password):
            raise exception

        return self.create_token(user)
