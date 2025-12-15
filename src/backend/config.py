from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Repo root: /workspaces/climate-insights-dashboard
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

CSV_PATH = DATA_DIR / "ga_clean.csv"
DB_PATH = DATA_DIR / "metro_metrics.db"


@dataclass(frozen=True)
class Settings:
    csv_path: Path = CSV_PATH
    db_path: Path = DB_PATH


settings = Settings()
