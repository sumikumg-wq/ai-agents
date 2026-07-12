"""
Central app configuration. All secrets come from environment variables —
never hardcode keys. Copy .env.example to .env and fill in values.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Chronicle AI Studio"
    environment: str = "development"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    youtube_client_id: str = ""
    youtube_client_secret: str = ""
    youtube_refresh_token: str = ""

    database_url: str = "sqlite:///./chronicle.db"

    cors_origins: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"


settings = Settings()
