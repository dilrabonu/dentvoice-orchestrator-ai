from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    log_level: str = "INFO"

    default_doctor: str = "MuhammadRaufxon"
    session_ttl_seconds: int = 3600

    pricing_mode: str = "NO_PRICE"

    # NEW:
    redis_url: str = "redis://localhost:6379/0"
    app_timezone: str = "Asia/Tashkent"


settings = Settings()