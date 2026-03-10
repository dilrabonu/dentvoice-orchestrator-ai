from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    log_level: str = "INFO"

    default_doctor: str = "MuhammadRaufxon"
    session_ttl_seconds: int = 3600

    pricing_mode: str = "NO_PRICE"

    redis_url: str = "redis://localhost:6379/0"
    app_timezone: str = "Asia/Tashkent"

    # NEW:
    public_base_url: str = "http://localhost:8000"
    twilio_stream_path: str = "/twilio/stream"
    twilio_incoming_path: str = "/twilio/incoming"


settings = Settings()