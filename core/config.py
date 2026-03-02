from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables / .env.
    """
    model_config = SettingConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    log_level: str = "INFO"

    default_doctor: str = "MuhammadRaufxon"
    session_ttl_seconds: int = 3600

    pricing_mode: str = "NO_PRICE"

settings = Settings()