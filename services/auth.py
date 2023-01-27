import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from config import settings
from db_config import create_session
from models import UserModel
from schemas.auth_schemas import Token, User, UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Получает текущего юзера на сайте с валидацией его токена"""

    return AuthService.validate_token(token)


class AuthService:
    """Класс аутентификации пользователя"""

    @classmethod
    def hash_password(cls, raw_password: str) -> str:
        """Хеширует пароль пользователя"""

        return bcrypt.hash(raw_password)

    @classmethod
    def verify_password(cls, password: str, hash_password: str) -> bool:
        """Проверяет введный пользователь пароль при аутентификации"""

        return bcrypt.verify(password, hash_password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        """Получает пользователя из JWT-токена и проверяет валидность"""

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
        """Генерирует JWT-токен для пользователя"""

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
        """Иницилизации сессии для работы с БД"""

        self.session = session

    def registration_user(self, user: UserCreate) -> Token:
        """Регистрация пользователя в БД"""

        user = UserModel(
            email=user.email,
            username=user.username,
            hash_password=self.hash_password(user.password)
        )

        self.session.add(user)
        self.session.commit()

        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        """Аутентификация пользователя в БД"""

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
