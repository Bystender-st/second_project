from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Загружаем .env ВРУЧНУЮ — обязательно для pydantic v2
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(ENV_PATH)


class Settings(BaseSettings):
    # env_file не указывается — оно игнорируется в pydantic v2
    model_config = SettingsConfigDict(env_prefix="")

    DATABASE_URL: str
    REDIS_URL: str
    MONGO_URL: str | None = "mongodb://mongo:27017"
    MONGO_DB_NAME: str = "delivery_logs"
    SECRET_KEY: str
    CBR_URL: str = "https://www.cbr-xml-daily.ru/daily_json.js"
    CORS_ORIGINS: str = "*"

    PAGE_SIZE_DEFAULT: int = 20


settings = Settings()
