📊 Metro Atlanta Inclusive Growth Dashboard

A full-stack data analytics application that visualizes inclusive economic growth across Metro Atlanta using the Mastercard Inclusive Growth Score (IGS) dataset.
The project combines FastAPI, SQLite, Streamlit, and CI/CD automation to deliver interactive insights for policymakers, researchers, and community stakeholders.

🔍 Project Overview
Goals

Build a full-stack web application to analyze inclusive growth metrics.

Enable exploration at both county and census tract levels.

Provide interactive visualizations to identify trends and disparities.

Support ethical, transparent data analysis.

Counties Included

Fulton County

DeKalb County

Cobb County

Clayton County

Years Analyzed

2020–2024

Key Metric Categories

Inclusive Growth

Economy

Place

Community

Net Occupancy

Affordable Housing

Internet Access

🏗️ Technical Architecture
climate-insights-dashboard/
│
├── src/
│   ├── backend/        # FastAPI backend
│   │   ├── app.py
│   │   ├── database.py
│   │   ├── load_data.py
│   │   └── config.py
│   │
│   └── frontend/       # Streamlit dashboard
│       └── dashboard.py
│
├── data/
│   ├── ga_clean.csv
│   └── metro_metrics.db
│
├── tests/              # Pytest test suite
│
├── .github/workflows/
│   └── ci.yml          # CI/CD pipeline
│
├── requirements.txt
├── README.md
└── diagrams/

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/dulli2k/mastercard-dashboard.git
cd climate-insights-dashboard

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt


Key Dependencies

fastapi

uvicorn

streamlit

pandas

sqlite3

pytest

flake8

requests

4️⃣ Load the Database

This creates the SQLite database from the cleaned CSV.

python -m src.backend.load_data


Database location:

data/metro_metrics.db

5️⃣ Start the FastAPI Backend
uvicorn src.backend.app:app --reload


API runs at: http://localhost:8000

Swagger Docs: http://localhost:8000/docs

6️⃣ Start the Streamlit Dashboard

In a new terminal:

streamlit run src/frontend/dashboard.py


Dashboard runs at:

http://localhost:8501

🔌 API Documentation
Base URL
http://localhost:8000

🔹 GET /health

Description: Health check
Response:

{ "status": "ok" }

🔹 GET /counties

Description: List all counties
Response:

["Clayton County", "Cobb County", "DeKalb County", "Fulton County"]

🔹 GET /years

Description: List available years
Response:

[2020, 2021, 2022, 2023, 2024]

🔹 GET /summary/county/{county}

Description: Yearly aggregated metrics for a county

Example:

/summary/county/Fulton County


Response:

{
  "county": "Fulton County",
  "years": [2020, 2021, 2022, 2023, 2024],
  "metrics": [
    {
      "year": 2020,
      "inclusive_growth_score": 54.3,
      "economy_score": 58.2,
      "place_score": 61.1
    }
  ]
}

🔹 GET /metrics/county/{county}?year=YYYY

Description: Tract-level metrics (optional year filter)

Example:

/metrics/county/Clayton County?year=2022

📊 Dashboard Usage Guide
Sidebar Filters

County: Select one of the four counties

Year: Filter tract-level table or view all years

Visualizations

Line Charts – Track trends over time

Bar Charts – Compare counties

Tables – Census tract–level metrics

Quick Stats – Average scores for selected county

Download CSV – Export filtered data

User Actions

✔ Compare counties
✔ Track growth trends (2020–2024)
✔ Identify disparities
✔ Download datasets

🧪 Testing & Code Quality
Run Tests
pytest

Run Linting
flake8 src


Coverage includes:

API endpoints

Database queries

Dashboard helpers

🚀 CI/CD Pipeline
GitHub Actions Workflow

Located at:

.github/workflows/ci.yml

Pipeline Stages

Install Dependencies

Run Pytest

Run flake8

Deploy Placeholder (Course Requirement)

Pipeline runs automatically on:

push

pull_request

☁️ Deployment (Optional / Future)

FastAPI

Google Cloud Run (Dockerized)

Render / Fly.io

Streamlit

Streamlit Community Cloud

Render

Current course version runs locally with deployment placeholders in CI/CD.

⚖️ Ethical Data Handling

No Personally Identifiable Information (PII)

Aggregated at census tract level

Avoids deficit-based neighborhood labeling

Transparent use of Mastercard IGS data

Contextual interpretation of disparities

👥 Team Contributions
Backend

FastAPI endpoints

SQLite schema & ingestion

Testing & API documentation

Frontend

Streamlit dashboard

Visualization design

CI/CD automation

Reporting & presentation

📌 License

Educational use only.