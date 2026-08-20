from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "app"
    debug: bool = False

    database_url: str
    redis_url: str
    rabbitmq_url: str
    jwt_secret: str = Field(min_length=12)
    meili_url: str
    meili_master_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()
