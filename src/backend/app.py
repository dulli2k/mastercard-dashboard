#Turn the database into a clean, documented web API that your Streamlit frontend (and tests) can call.
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .database import fetch_all, fetch_one

app = FastAPI(
    title="Metro Atlanta Inclusive Growth API",
    description=(
        "FastAPI backend for Mastercard Inclusive Growth Score data "
        "for Fulton, DeKalb, Cobb, and Clayton counties."
    ),
    version="1.0.0",
)

# CORS for Streamlit + dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> Dict[str, str]:
    """Simple health check."""
    return {"status": "ok"}


@app.get("/counties", response_model=List[str])
def list_counties() -> List[str]:
    """Return list of distinct counties in the dataset."""
    rows = fetch_all("SELECT DISTINCT county FROM metro_metrics ORDER BY county;")
    return [r["county"] for r in rows]


@app.get("/years", response_model=List[int])
def list_years() -> List[int]:
    """Return list of distinct years in the dataset."""
    rows = fetch_all("SELECT DISTINCT year FROM metro_metrics ORDER BY year;")
    return [int(r["year"]) for r in rows if r["year"] is not None]


@app.get("/summary/county/{county_name}")
def summary_by_county(county_name: str) -> Dict[str, Any]:
    """
    Aggregated metrics by year for a single county.
    Used for line charts in Streamlit.
    """
    sql = """
        SELECT
            year,
            AVG(inclusive_growth_score)      AS inclusive_growth_score,
            AVG(economy_score)              AS economy_score,
            AVG(place_score)                AS place_score,
            AVG(community_score)            AS community_score,
            AVG(net_occupancy_score)        AS net_occupancy_score,
            AVG(affordable_housing_score)   AS affordable_housing_score,
            AVG(internet_access_score)      AS internet_access_score
        FROM metro_metrics
        WHERE county = ?
        GROUP BY year
        ORDER BY year;
    """
    rows = fetch_all(sql, (county_name,))
    if not rows:
        raise HTTPException(status_code=404, detail="County not found or no data.")

    return {
        "county": county_name,
        "years": [int(r["year"]) for r in rows],
        "metrics": rows,
    }

@app.get("/metrics/county/{county_name}")
def metrics_for_county(
    county_name: str,
    year: int | None = Query(default=None, description="Optional year filter"),
) -> Dict[str, Any]:
    """
    Raw metrics for all tracts in a county.
    Optional ?year=2022 filter.
    """
    base_sql = """
        SELECT
            census_tract_fips,
            county,
            state,
            year,
            inclusive_growth_score,
            economy_score,
            place_score,
            community_score,
            net_occupancy_score,
            affordable_housing_score,
            internet_access_score
        FROM metro_metrics
        WHERE county = ?
    """

    params: list[Any] = [county_name]

    if year is not None:
        base_sql += " AND year = ?"
        params.append(year)

    base_sql += " ORDER BY year, census_tract_fips;"

    rows = fetch_all(base_sql, tuple(params))

    if not rows:
        raise HTTPException(status_code=404, detail="No data for this county/year.")

    return {
        "county": county_name,
        "year": year,
        "count": len(rows),
        "rows": rows,
    }


@app.get("/metrics/tract/{census_tract_fips}")
def metrics_for_tract(census_tract_fips: str) -> Dict[str, Any]:
    """
    Time series for a single census tract.
    """
    sql = """
        SELECT
            census_tract_fips,
            county,
            state,
            year,
            inclusive_growth_score,
            economy_score,
            place_score,
            community_score,
            net_occupancy_score,
            affordable_housing_score,
            internet_access_score
        FROM metro_metrics
        WHERE census_tract_fips = ?
        ORDER BY year;
    """
    rows = fetch_all(sql, (census_tract_fips,))

    if not rows:
        raise HTTPException(status_code=404, detail="No data for this census tract.")

    return {
        "census_tract_fips": census_tract_fips,
        "rows": rows,
    }
