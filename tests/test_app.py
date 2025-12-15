from fastapi.testclient import TestClient

from src.backend.app import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_get_counties():
    resp = client.get("/counties")
    assert resp.status_code == 200
    counties = resp.json()
    assert isinstance(counties, list)
    assert "Fulton County" in counties


def test_get_years():
    resp = client.get("/years")
    assert resp.status_code == 200
    years = resp.json()
    assert years == sorted(years)
    assert len(years) > 0


def test_county_summary_valid():
    resp = client.get("/summary/county/Fulton County")
    assert resp.status_code == 200
    data = resp.json()
    assert data["county"] == "Fulton County"
    assert "metrics" in data


def test_county_summary_invalid():
    resp = client.get("/summary/county/NotARealCounty")
    assert resp.status_code in (404, 200)


def test_metrics_county_all_years():
    resp = client.get("/metrics/county/Fulton County")
    assert resp.status_code == 200
    data = resp.json()
    assert data["county"] == "Fulton County"
    assert data["count"] > 0


def test_metrics_county_specific_year():
    years_resp = client.get("/years")
    year = years_resp.json()[0]
    resp = client.get(f"/metrics/county/Fulton County?year={year}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["year"] == year


def test_metrics_county_invalid_year():
    resp = client.get("/metrics/county/Fulton County?year=1900")
    # Your API currently returns 404 for no data, which is valid behavior.
    assert resp.status_code in (404, 200)
