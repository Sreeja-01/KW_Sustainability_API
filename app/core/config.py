"""
Application configuration and settings.
Load from .env file.
"""

from typing import Any, Dict, Optional
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API
    PROJECT_NAME: str = "KW Sustainability Data API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "kw_sustainability"
    ECHO_QUERIES: bool = False

    # LLM - GROQ
    LLM_PROVIDER: str = "groq"
    # DO NOT hardcode key here; put in .env
    GROQ_API_KEY: str = ""
    LLM_MODEL: str = "llama3-70b-8192"
    LLM_MAX_TOKENS: int = 4000
    LLM_TEMPERATURE: float = 0.1

    # Auth
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60
    ALGORITHM: str = "HS256"

    # File upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024
    UPLOAD_DIR: str = "app/uploads"

    # Database URL
    @property
    def DATABASE_URL(self) -> str:
        """Database connection URL."""
        return self.SQLALCHEMY_DATABASE_URI

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Dynamic database URI property."""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
