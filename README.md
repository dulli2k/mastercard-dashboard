# 📊 Metro Atlanta Inclusive Growth Dashboard

A full-stack data visualization application analyzing inclusive economic growth across Metro Atlanta using the Mastercard Inclusive Growth Score (IGS) dataset.

---

## 📌 Project Overview

The Metro Atlanta Inclusive Growth Dashboard is a full-stack web application designed to help users explore economic, housing, infrastructure, and community well-being trends across Metro Atlanta.

This project enables policymakers, researchers, and residents to:
- Compare counties and census tracts over time
- Identify disparities in economic inclusion
- Explore trends across housing, economy, and infrastructure

---

## 📂 Dataset Description

**Dataset Used:** Mastercard Inclusive Growth Score (IGS)

**Geographic Scope:**
- Fulton County
- DeKalb County
- Cobb County
- Clayton County

**Years Covered:** 2020–2024

**Key Metric Categories:**
- Inclusive Growth Score
- Economy
- Place
- Community
- Net Occupancy
- Affordable Housing
- Internet Access
- Small Business Activity
- Travel Time to Work

All data is aggregated at the census tract level and contains no personally identifiable information (PII).

---

## 🏗 Technical Architecture

### Backend (FastAPI + SQLite)

- FastAPI serves as the REST API backend.
- Cleaned CSV data is loaded into a local SQLite database.
- SQL queries power all API endpoints.
- Automatic OpenAPI documentation available at `/docs`.

**Backend Files:**
- `app.py` — API routes and request handling
- `database.py` — SQLite connection and query helpers
- `load_data.py` — Loads cleaned CSV into SQLite

---

### Frontend (Streamlit Dashboard)

- Streamlit provides an interactive UI.
- Dashboard fetches live data from FastAPI via HTTP requests.
- Users can filter by county and year.
- Charts and tables update dynamically.

**Frontend Features:**
- Line charts for year-over-year trends
- Bar charts comparing counties
- Census tract–level tables
- CSV download option

---

## 🔌 API Documentation

### Health Check
```
GET /health
```
**Response**
```
{ "status": "ok" }
```

---

### List Counties
```
GET /counties
```
**Response**
```
["Clayton County", "Cobb County", "DeKalb County", "Fulton County"]
```

---

### List Years
```
GET /years
```
**Response**
```
[2020, 2021, 2022, 2023, 2024]
```

---

### County Summary
```
GET /summary/county/{county_name}
```

Returns yearly averages for key metrics used in trend visualizations.

---

### County Metrics (Tract-Level)
```
GET /metrics/county/{county_name}?year=2023
```

Returns census tract–level metrics for a given county and optional year.

---

## 📈 Dashboard Usage Guide

1. Start the FastAPI backend:
```
uvicorn src.backend.app:app --reload
```

2. Launch the Streamlit dashboard:
```
streamlit run src/frontend/dashboard.py
```

3. Use the sidebar to:
- Select a county
- Filter by year (or view all years)

4. Explore:
- Yearly trend charts
- Tract-level data tables
- County comparisons

5. Download filtered data as CSV for further analysis.

---

## ⚖️ Ethical Considerations & Bias Mitigation

- No PII — all data is aggregated at the census tract level.
- Privacy-first design — no demographic labeling of individuals.
- No stigmatization — avoids ranking neighborhoods as “good” or “bad.”
- Contextual interpretation — metrics reflect structural inequities, not individual failure.
- Transparency — all scores come directly from Mastercard IGS.

---

## 🔁 CI/CD Pipeline

This project includes a GitHub Actions CI/CD pipeline that:
- Runs Pytest for backend and frontend tests
- Enforces PEP 8 standards using flake8
- Validates builds on every push and pull request
- Includes a placeholder deploy stage for course requirements

**Workflow File:**
```
.github/workflows/ci.yml
```

---

## 🚀 Deployment Instructions

### Local Deployment

**Backend**
```
uvicorn src.backend.app:app --reload
```

**Frontend**
```
streamlit run src/frontend/dashboard.py
```

---

### CI/CD Deployment (Course Placeholder)

- Tests and linting run automatically on GitHub.
- Deployment step currently logs success (no cloud deployment required).
- Pipeline structure supports future deployment to cloud services.

---

## 👥 Team Contributions

### Backend Lead
- Designed FastAPI endpoints
- Built SQLite schema
- Implemented data loading and testing
- Optimized query performance

### Frontend Lead
- Built Streamlit dashboard UI
- Integrated API responses
- Implemented interactive charts and tables
- Developed CI/CD pipeline and documentation

---

## 📜 License

This project is for educational purposes and uses publicly available data from the Mastercard Inclusive Growth Score.
