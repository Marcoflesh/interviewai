"""Configuracion por variables de entorno (ver .env.example)."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://interviewai:interviewai@db:5432/interviewai"
    llm_provider: str = "fake"      # fake | gemini | openai  (RIN-01)
    llm_model: str = ""
    gemini_api_key: str = ""
    openai_api_key: str = ""
    json_retry_attempts: int = 1    # RF-03 flujo 6A: un reintento automatico
    auth_mode: str = "dev"          # dev = cabecera X-Role (SOLO desarrollo). TODO T-114


settings = Settings()
