from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    APP_ENV: str = "development"
    APP_NAME: str = "YouTube Clipper API"
    APP_VERSION: str = "1.0.0"

    MONGODB_URI: str
    REDIS_URL: str

    # DigitalOcean Spaces (S3 compatible) preferred names.
    STORAGE_BUCKET: str = Field(
        validation_alias=AliasChoices("SPACES_BUCKET", "AWS_S3_BUCKET")
    )
    STORAGE_ACCESS_KEY: str = Field(
        validation_alias=AliasChoices("SPACES_ACCESS_KEY", "AWS_ACCESS_KEY_ID")
    )
    STORAGE_SECRET_KEY: str = Field(
        validation_alias=AliasChoices("SPACES_SECRET_KEY", "AWS_SECRET_ACCESS_KEY")
    )
    STORAGE_REGION: str = Field(
        validation_alias=AliasChoices("SPACES_REGION", "AWS_REGION")
    )
    STORAGE_ENDPOINT: str = Field(
        validation_alias=AliasChoices("SPACES_ENDPOINT", "AWS_S3_ENDPOINT")
    )

    SIGNED_URL_TTL_SECONDS: int = 3600
    ALLOWED_ORIGINS: str = "*"

    @field_validator("STORAGE_ENDPOINT", mode="before")
    @classmethod
    def strip_endpoint_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/") if isinstance(value, str) else value

    @property
    def allowed_origins_list(self) -> list[str]:
        items = [item.strip() for item in self.ALLOWED_ORIGINS.split(",") if item.strip()]
        return items or ["*"]


settings = Settings()