"""Central configuration, loaded from environment variables (.env)."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"
    tenant_id: str = "safir-tishlar"

    redis_url: str = "redis://localhost:6379/0"
    session_ttl_seconds: int = 3600

    database_url: str = "postgresql://dentvoice:dentvoice@localhost:5432/dentvoice"

    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

    whisper_model: str = "large-v3"
    tts_provider: str = "azure"
    tts_api_key: str = ""

    anthropic_api_key: str = ""

    default_doctor: str = "MuhammadRaufxon"
    stt_confidence_threshold: float = 0.75
    latency_target_seconds: float = 2.5


settings = Settings()