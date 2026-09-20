from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "bookshop"
    debug: bool = False
    log_level: str = "ERROR"
    mongo_url: str = "mongodb://localhost:27017"
    mongo_database: str = "bookshop"
    mongo_transactions: bool = False
    redis_url: str = "redis://localhost:6379/0"
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    jwt_secret: str = Field(default="development-secret-key-change-me", min_length=12)
    meili_url: str = "http://localhost:7700"
    meili_master_key: str = "development-key"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
