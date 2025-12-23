import os
from functools import lru_cache

from dotenv import load_dotenv


load_dotenv()


class Settings:
    PROJECT_NAME: str = "InterviewDost API"
    ENV: str = os.getenv("ENV", "development")

    # DB: default to local SQLite for dev; override with PostgreSQL URL in env
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./interviewdost.db",
    )

    # LLM / Tavus placeholders for later wiring
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")
    TAVUS_API_KEY: str | None = os.getenv("TAVUS_API_KEY")


@lru_cache
def get_settings() -> Settings:
    return Settings()
