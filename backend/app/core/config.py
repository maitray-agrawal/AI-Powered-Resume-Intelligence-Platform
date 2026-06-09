from typing import List, Union
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Intelligence Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "secret_key_for_security_should_be_changed_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    UPLOAD_DIR: str = "uploads"

    # Database Settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "resume_intelligence"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/resume_intelligence"

    # Chroma Vector Database Settings
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000

    # Gemini API Settings
    GEMINI_API_KEY: Union[str, None] = None

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
