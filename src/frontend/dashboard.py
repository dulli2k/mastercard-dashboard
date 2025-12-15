from __future__ import annotations

import pandas as pd
import requests
import streamlit as st

API_URL = "http://localhost:8000"


@st.cache_data
def get_counties() -> list[str]:
    resp = requests.get(f"{API_URL}/counties", timeout=30)
    resp.raise_for_status()
    return resp.json()


@st.cache_data
def get_years() -> list[int]:
    resp = requests.get(f"{API_URL}/years", timeout=30)
    resp.raise_for_status()
    return resp.json()


@st.cache_data
def get_summary(county: str) -> dict:
    resp = requests.get(f"{API_URL}/summary/county/{county}", timeout=30)
    resp.raise_for_status()
    return resp.json()


@st.cache_data
def get_county_metrics(county: str, year: int | None = None) -> dict:
    params: dict = {}
    if year is not None:
        params["year"] = year

    resp = requests.get(
        f"{API_URL}/metrics/county/{county}",
        params=params,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    st.set_page_config(
        page_title="Metro Atlanta Inclusive Growth Dashboard",
        layout="wide",
    )

    st.title("📊 Metro Atlanta Inclusive Growth Dashboard")
    st.markdown(
        """
This dashboard uses Mastercard **Inclusive Growth Score** data for
**Fulton, DeKalb, Cobb, and Clayton Counties** (Metro Atlanta).

Use the sidebar controls to explore trends over time and compare
high-level metrics across counties.
        """
    )

    counties = get_counties()
    years = get_years()

    st.sidebar.header("Filters")
    county = st.sidebar.selectbox("County", counties)
    year_filter = st.sidebar.selectbox(
        "Year (for tract table)",
        ["All"] + years,
    )

    year_value = None if year_filter == "All" else int(year_filter)

    summary = get_summary(county)
    metrics_df = pd.DataFrame(summary["metrics"])

    st.subheader(f"Yearly Inclusive Growth Metrics — {county}")

    metric_to_plot = st.selectbox(
        "Metric to visualize",
        [
            "inclusive_growth_score",
            "economy_score",
            "place_score",
            "community_score",
            "net_occupancy_score",
            "affordable_housing_score",
            "internet_access_score",
        ],
        index=0,
    )

    if not metrics_df.empty:
        chart_df = metrics_df[["year", metric_to_plot]].set_index("year")
        st.line_chart(chart_df)

    st.subheader("Tract-level metrics")

    metrics = get_county_metrics(county, year_value)
    tracts_df = pd.DataFrame(metrics["rows"])

    if not tracts_df.empty:
        st.dataframe(tracts_df)

        st.subheader("Quick stats")
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Avg Inclusive Growth Score",
            f"{tracts_df['inclusive_growth_score'].mean():.1f}",
        )
        col2.metric(
            "Avg Affordable Housing Score",
            f"{tracts_df['affordable_housing_score'].mean():.1f}",
        )
        col3.metric(
            "Avg Internet Access Score",
            f"{tracts_df['internet_access_score'].mean():.1f}",
        )

        csv_bytes = tracts_df.to_csv(index=False).encode("utf-8")
        file_stub = county.replace(" ", "_").lower()
        year_stub = "all_years" if year_value is None else str(year_value)
        filename = f"{file_stub}_{year_stub}_metrics.csv"

        st.download_button(
            label="Download data as CSV",
            data=csv_bytes,
            file_name=filename,
            mime="text/csv",
        )

    st.subheader("County comparison (latest year)")
    latest_year = max(years)

    comparison_rows: list[dict] = []
    for cty in counties:
        data = get_county_metrics(cty, latest_year)
        df_cty = pd.DataFrame(data["rows"])
        if not df_cty.empty:
            comparison_rows.append(
                {
                    "County": cty,
                    "Avg Inclusive Growth Score": (
                        df_cty["inclusive_growth_score"].mean()
                    ),
                }
            )

    if comparison_rows:
        comparison_df = pd.DataFrame(comparison_rows).set_index("County")
        st.bar_chart(comparison_df)


if __name__ == "__main__":
    main()
