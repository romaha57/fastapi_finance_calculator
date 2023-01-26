from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models import UserModel
from schemas.auth_schemas import UserCreate, Token, User

from services.auth import AuthService, get_current_user

auth_router = APIRouter(prefix="/auth", tags=["Users"])


@auth_router.post("/register", response_model=Token)
def register_user(
        auth_data: UserCreate,
        service: AuthService = Depends()):

    """Регистрация пользователя"""

    return service.registration_user(auth_data)


@auth_router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends()):

    """Аутентификация пользователя"""

    return service.authenticate_user(
        username=form_data.username,
        password=form_data.password
    )


@auth_router.get("/user", response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user
