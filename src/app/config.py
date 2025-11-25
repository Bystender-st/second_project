# src/app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # we use the already existing env variable names (from step 1)
    DATABASE_URL: str
    REDIS_URL: str
    MONGO_URL: Optional[str] = None
    SECRET_KEY: str
    CBR_URL: str = "https://www.cbr-xml-daily.js"
    CORS_ORIGINS: str = "*"

    PAGE_SIZE_DEFAULT: int = 20


settings = Settings()
