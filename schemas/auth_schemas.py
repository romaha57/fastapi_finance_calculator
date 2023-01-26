from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    username: str

    class Config:
        arbitrary_types_allowed = True


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class UserCreate(BaseUser):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
