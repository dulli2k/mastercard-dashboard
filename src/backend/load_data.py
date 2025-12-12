#One-time ETL script that takes the cleaned CSV and loads it into the SQLite database with the exact schema your backend expects.
import sqlite3

import pandas as pd

from .config import CSV_PATH, DB_PATH


def main() -> None:
    # 1. Load cleaned CSV
    df = pd.read_csv(CSV_PATH)

    # Map CSV column names → DB column names used by the API
    rename_map = {
        "Census Tract FIPS code": "census_tract_fips",
        "County": "county",
        "State": "state",
        "Year": "year",

        # Main Scores
        "Inclusive Growth Score": "inclusive_growth_score",
        "Economy": "economy_score",
        "Place": "place_score",
        "Community": "community_score",

        # Additional key metrics
        "Net Occupancy Score": "net_occupancy_score",
        "Affordable Housing Score": "affordable_housing_score",
        "Internet Access Score": "internet_access_score",
    }

    # Safety check: make sure all expected columns exist in the CSV
    missing = [col for col in rename_map.keys() if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    # Rename columns and keep only what we need
    df = df.rename(columns=rename_map)
    df = df[list(rename_map.values())]

    # 2. Create / reset SQLite DB
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()


    #Drop and recreate the table
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

    # 3. Bulk insert the datafram into sqlite
    df.to_sql("metro_metrics", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()
    print(f"Loaded {len(df)} rows into {DB_PATH}")


if __name__ == "__main__":
    main()
