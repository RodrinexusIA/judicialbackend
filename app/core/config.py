from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "judicial-backend"
    ENV: str = "dev"

    DATABASE_URL: str
    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    DATAJUD_API_KEY: str
    DATAJUD_TJGO_URL: str

    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
