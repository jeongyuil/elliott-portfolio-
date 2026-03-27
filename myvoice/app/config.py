"""
MyVoice (밤토리) - Voice AI Education Platform
Settings configuration using Pydantic BaseSettings.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import model_validator


class Settings(BaseSettings):
    # App
    app_name: str = "MyVoice API"
    app_env: str = "development"
    debug: bool = True
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Database
    database_url: str = "postgresql+asyncpg://myvoice:myvoice_dev@localhost:5432/myvoice"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str = "dev-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours

    # OpenAI
    openai_api_key: str = ""

    # Anthropic (Claude)
    anthropic_api_key: str = ""

    # URLs
    app_base_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:5173"

    # Resend (email service)
    resend_api_key: str = ""
    email_from: str = "no-reply@bamtory.com"
    email_from_name: str = "밤토리"

    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""

    # Kakao OAuth
    kakao_client_id: str = ""
    kakao_client_secret: str = ""

    # Apple Sign In
    apple_team_id: str = ""
    apple_key_id: str = ""
    apple_private_key: str = ""  # PEM 형식 (줄바꿈은 \n으로)
    apple_bundle_id: str = ""

    # Voice Mode: "realtime" (OpenAI Realtime API) | "azure" (Azure Realtime) | "http" (legacy Whisper+GPT+TTS)
    voice_mode: str = "realtime"

    # OpenAI Realtime API (for realtime mode - movice pattern)
    realtime_model: str = "gpt-4o-mini-realtime-preview"
    realtime_voice: str = "shimmer"  # 밝고 친근한 아이 친화적 목소리
    realtime_speech_rate: float = 1.0

    # Azure OpenAI Realtime API (for azure mode)
    azure_realtime_api_key: str = ""
    azure_realtime_endpoint: str = ""
    azure_realtime_api_version: str = "2025-04-01-preview"
    azure_realtime_deployment: str = "gpt-4o-realtime-preview"

    # Azure Whisper (for azure mode STT)
    azure_whisper_api_key: str = ""
    azure_whisper_endpoint: str = ""
    azure_whisper_api_version: str = "2024-06-01"
    azure_whisper_deployment: str = "whisper"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    @model_validator(mode='after')
    def validate_secrets(self):
        if self.app_env == "production":
            if "change" in self.jwt_secret_key or "dev-secret" in self.jwt_secret_key:
                raise ValueError("JWT_SECRET_KEY must be changed in production")
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required in production")
            if not self.resend_api_key or "your_api_key" in self.resend_api_key:
                raise ValueError("RESEND_API_KEY is required in production")
            if self.voice_mode == "realtime" and not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when VOICE_MODE=realtime")
            if self.voice_mode == "azure":
                if not self.azure_realtime_api_key:
                    raise ValueError("AZURE_REALTIME_API_KEY is required when VOICE_MODE=azure")
                if not self.azure_realtime_endpoint:
                    raise ValueError("AZURE_REALTIME_ENDPOINT is required when VOICE_MODE=azure")
        return self

    @property
    def redis_host(self) -> str:
        from urllib.parse import urlparse
        return urlparse(self.redis_url).hostname or "localhost"

    @property
    def redis_port(self) -> int:
        from urllib.parse import urlparse
        return urlparse(self.redis_url).port or 6379


@lru_cache()
def get_settings() -> Settings:
    return Settings()
