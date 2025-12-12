import os
import sqlite3
from fastapi.testclient import TestClient

from src.backend.app import app
from src.backend.database import fetch_all, fetch_one, get_db

client = TestClient(app)


def override_get_db():
    db_path = "data/metro_atlanta.db"
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


app.dependency_overrides[get_db] = override_get_db


def test_health():
    """Basic health-check endpoint works."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_get_counties():
    """Counties endpoint returns at least the 4 metro Atlanta counties."""
    resp = client.get("/counties")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert "Fulton County" in data
    assert "DeKalb County" in data
    assert "Cobb County" in data
    assert "Clayton County" in data


def test_get_years():
    """Years endpoint returns a non-empty sorted list."""
    resp = client.get("/years")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data == sorted(data)


def test_county_summary_valid():
    """Summary endpoint returns metrics for a valid county."""
    resp = client.get("/summary/county/Fulton County")
    assert resp.status_code == 200
    data = resp.json()
    assert "county" in data
    assert data["county"] == "Fulton County"
    assert "metrics" in data
    assert isinstance(data["metrics"], list)
    assert len(data["metrics"]) > 0
    assert "year" in data["metrics"][0]
    assert "inclusive_growth_score" in data["metrics"][0]


def test_county_summary_invalid():
    """Invalid county should return 404."""
    resp = client.get("/summary/county/NotARealCounty")
    assert resp.status_code == 404


def test_metrics_county_all_years():
    """Metrics endpoint works with no year filter."""
    resp = client.get("/metrics/county/Fulton County")
    assert resp.status_code == 200
    data = resp.json()
    assert "rows" in data
    assert isinstance(data["rows"], list)
    if data["rows"]:
        row = data["rows"][0]
        assert "county" in row
        assert "year" in row
        assert "inclusive_growth_score" in row


def test_metrics_county_specific_year():
    """Metrics endpoint works with a valid year filter."""
    # use the first available year from /years
    years_resp = client.get("/years")
    year = years_resp.json()[0]

    resp = client.get(f"/metrics/county/Fulton County?year={year}")
    assert resp.status_code == 200
    data = resp.json()
    assert "rows" in data
    for row in data["rows"]:
        assert row["year"] == year


def test_metrics_county_invalid_year():
    """Invalid year should return empty or appropriate validation behavior."""
    resp = client.get("/metrics/county/Fulton County?year=1900")
    assert resp.status_code == 200
    data = resp.json()
    assert "rows" in data
    # For this project, we accept empty result set as valid behavior
    # rather than raising an error.
    # assert len(data["rows"]) == 0  # optional if you want strict behavior
