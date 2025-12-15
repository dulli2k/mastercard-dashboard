import sqlite3
from pathlib import Path
import pandas as pd

from .config import settings


# --- Paths ---------------------------------------------------------
BASE_DIR = settings.BASE_DIR
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

CSV_PATH = DATA_DIR / "ga_clean.csv"
DB_PATH = settings.DB_PATH


def main() -> None:
    df = pd.read_csv(CSV_PATH)

    rename_map = {
        "Census Tract FIPS code": "census_tract_fips",
        "County": "county",
        "State": "state",
        "Year": "year",
        "Inclusive Growth Score": "inclusive_growth_score",
        "Economy": "economy_score",
        "Place": "place_score",
        "Community": "community_score",
        "Net Occupancy Score": "net_occupancy_score",
        "Affordable Housing Score": "affordable_housing_score",
        "Internet Access Score": "internet_access_score",
    }

    df = df.rename(columns=rename_map)
    df = df[list(rename_map.values())]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS metro_metrics;")

    cur.execute(
        """
        CREATE TABLE metro_metrics (
            census_tract_fips TEXT,
            county TEXT,
            state TEXT,
            year INTEGER,
            inclusive_growth_score REAL,
            economy_score REAL,
            place_score REAL,
            community_score REAL,
            net_occupancy_score REAL,
            affordable_housing_score REAL,
            internet_access_score REAL
        );
        """
    )

    df.to_sql("metro_metrics", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()

    print(f"Loaded {len(df)} rows into {DB_PATH}")


if __name__ == "__main__":
    main()
