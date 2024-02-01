from pathlib import Path

from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings class.

    Subclass of the pydantic settings BaseSettings class.
    """

    PROJECT_NAME: str = "IS74 Image Processing Service"
    API_STR: str = "/api"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # Redis (host & port receiving from .env file)
    REDIS_HOST: str = "1"
    REDIS_PORT: str = "2"
    REDIS_URL: RedisDsn | None = None

    @field_validator("REDIS_URL", mode="before")
    @classmethod
    def _build_redis_url(cls, v, info: FieldValidationInfo) -> str:
        """Build the Redis URL based on provided configuration."""

        redis_host = info.data.get("REDIS_HOST")
        redis_port = info.data.get("REDIS_PORT")

        return f"redis://{redis_host}:{redis_port}"

    # DB
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "2580"
    POSTGRES_DB: str = "is74"
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    # ML service
    ML_SERVICE_URL: str = "http://ml_service:5000/ml-process-img"

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def _build_postgres_uri(cls, v, info: FieldValidationInfo):
        """
        Build the PostgreSQL URI based on provided configuration.

        Args:
            v: The field value.
            info (FieldValidationInfo): Information about the validation.

        Returns:
            str: The constructed PostgreSQL URI.
        """
        postgres_user = info.data.get("POSTGRES_USER")
        postgres_password = info.data.get("POSTGRES_PASSWORD")
        postgres_server = info.data.get("POSTGRES_SERVER")
        postgres_db = info.data.get("POSTGRES_DB")

        return (
            f"postgresql+asyncpg://{postgres_user}:{postgres_password}"
            f"@{postgres_server}:5432/{postgres_db}"
        )

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=BASE_DIR.parent.parent / "deployment" / ".env.img_service",
    )


def get_settings() -> Settings:
    """Get Settings instance."""
    return Settings()


settings = get_settings()
