from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    """Базовая модель пользователя для аутентификации"""

    email: EmailStr
    username: str

    class Config:
        arbitrary_types_allowed = True


class User(BaseUser):
    """Модель пользователя для отображения"""

    id: int

    class Config:
        orm_mode = True


class UserCreate(BaseUser):
    """Модель пользователя для создания пользователя"""

    password: str


class Token(BaseModel):
    """Модель JWT-токена для аутентификации"""

    access_token: str
    token_type: str = 'bearer'
