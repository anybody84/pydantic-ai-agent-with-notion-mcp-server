from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    notion_token: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_model_temperature: float = 0.0


class LocalAppSettings(AppSettings):
    def __init__(self):
        super().__init__()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> AppSettings:
    return LocalAppSettings()


settings = get_settings()
