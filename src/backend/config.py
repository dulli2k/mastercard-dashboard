#One place to define paths and shared settings so every other backend file can agree on where things live.
from pathlib import Path

# Project root: /workspaces/climate-insights-dashboard
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

CSV_PATH = DATA_DIR / "ga_clean.csv"
DB_PATH = DATA_DIR / "metro_metrics.db"
