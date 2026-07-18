"""Application configuration placeholder."""

from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Question
AppEnv = Literal["local", "test", "production"]
# Question -- critical
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    #question -- use of alias
    app_name: str = Field(default="crypto-investment-agentic-system", alias="APP_NAME")
    app_env: AppEnv = Field(default="local", alias="APP_ENV")
    log_level: LogLevel = Field(default="INFO", alias="LOG_LEVEL")

    bithumb_base_url: AnyHttpUrl = Field(
        default="https://api.bithumb.com",
        alias="BITHUMB_BASE_URL",
    )

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    request_timeout_seconds: float = Field(
        default=30.0,
        alias="REQUEST_TIMEOUT_SECONDS",
        gt=0,
    )

#question
@lru_cache
def get_settings() -> Settings:
    return Settings()