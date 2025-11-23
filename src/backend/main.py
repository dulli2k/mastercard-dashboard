# src/backend/main.py
from fastapi import FastAPI

app = FastAPI(title="Mastercard Inclusive Growth API")

@app.get("/")
def root():
    return {"status": "ok", "message": "API is running"}

@app.get("/growth/summary")
def growth_summary():
    return {"detail": "Inclusive growth summary placeholder"}

@app.get("/spending")
def spending(region: str = None, year: int = None):
    return {"region": region, "year": year, "detail": "Spending data placeholder"}

@app.get("/business/health")
def business_health(zip: str):
    return {"zip": zip, "detail": "Business vitality placeholder"}

@app.get("/correlation")
def correlation():
    return {"detail": "Correlation analysis placeholder"}
