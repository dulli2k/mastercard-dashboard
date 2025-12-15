# src/backend/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central app settings.

    Reads optional environment variables, but also provides safe defaults
    for local development + Codespaces.
    """

    # repo root is 2 levels above src/backend/config.py => .../src/backend/ -> .../
    BASE_DIR: Path = Path(__file__).resolve().parents[2]

    # Default SQLite DB path (matches your loader)
    DB_PATH: Path = BASE_DIR / "data" / "metro_metrics.db"

    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")


# ✅ This is what tests expect to import
settings = Settings()
