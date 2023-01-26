from pydantic import BaseSettings


class Settings(BaseSettings):
    server_port = 8000
    database_url: str = "sqlite:///./database.db"
    jwt_algorithm: str = "HS256"
    jwt_secret: str
    jwt_expiration: int = 3600


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8"
)