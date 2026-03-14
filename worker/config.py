import os
from dotenv import load_dotenv, find_dotenv
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load env as early as possible
load_dotenv(find_dotenv())


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    MONGODB_URI: str
    REDIS_URL: str

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


settings = Settings()

MONGODB_URI = settings.MONGODB_URI
REDIS_URL = settings.REDIS_URL

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI is not set")

if not REDIS_URL:
    raise RuntimeError("REDIS_URL is not set")
