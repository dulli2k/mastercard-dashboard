# Give users an interactive UI to choose a county/year and visualize what the API returns.
import requests
import numpy as np
import pandas as pd
import streamlit as st

API_URL = "http://localhost:8000"  # FastAPI base URL


# Helper functions to call the API
@st.cache_data
def get_counties():
    resp = requests.get(f"{API_URL}/counties")
    resp.raise_for_status()
    return resp.json()


@st.cache_data
def get_years():
    resp = requests.get(f"{API_URL}/years")
    resp.raise_for_status()
    return resp.json()


@st.cache_data
def get_summary(county: str):
    resp = requests.get(f"{API_URL}/summary/county/{county}")
    resp.raise_for_status()
    return resp.json()


@st.cache_data
def get_county_metrics(county: str, year: int | None = None):
    params = {}
    if year is not None:
        params["year"] = year
    resp = requests.get(f"{API_URL}/metrics/county/{county}", params=params)
    resp.raise_for_status()
    return resp.json()


def main():
    st.set_page_config(
        page_title="Metro Atlanta Inclusive Growth Dashboard",
        layout="wide",
    )

    st.title("📊 Metro Atlanta Inclusive Growth Dashboard")
    st.markdown(
        """
        This dashboard uses Mastercard **Inclusive Growth Score** data for  
        **Fulton, DeKalb, Cobb, and Clayton Counties** (Metro Atlanta).

        Use the controls in the sidebar to explore trends over time and compare
        high-level metrics across counties.
        """
    )

    # Sidebar controls
    counties = get_counties()
    years = get_years()

    st.sidebar.header("Filters")
    county = st.sidebar.selectbox("County", counties)
    year_filter = st.sidebar.selectbox(
        "Year (for tract-level table)", ["All"] + years
    )
    year_value = None if year_filter == "All" else int(year_filter)

    # ----- Summary line chart -----------------------------------------
    summary = get_summary(county)
    metrics_df = pd.DataFrame(summary["metrics"])

    st.subheader(f"Yearly Inclusive Growth Metrics – {county}")
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

    # --- Tract-level table --------------------------------------------
    st.subheader("Tract-level metrics")

    # Call backend metrics endpoint (this was get_metrics before)
    metrics = get_county_metrics(county, year_value)

    # Make a DataFrame from API rows
    table_df = pd.DataFrame(metrics["rows"])

    # Filter by year on the frontend (if a specific year is selected)
    if year_value is not None:
        filtered_df = table_df[table_df["year"] == year_value]
    else:
        filtered_df = table_df

    # Show table in dashboard
    st.dataframe(filtered_df)

    # --- County comparison bar chart (latest year) --------------------
    latest_year = max(years) if years else None
    comparison_rows = []

    if latest_year is not None:
        for c in counties:
            data = get_county_metrics(c, latest_year)
            df_c = pd.DataFrame(data["rows"])
            if not df_c.empty:
                comparison_rows.append(
                    {
                        "County": c,
                        "Avg Inclusive Growth Score": df_c[
                            "inclusive_growth_score"
                        ].mean(),
                    }
                )

    if comparison_rows:
        comparison_df = pd.DataFrame(comparison_rows).set_index("County")
        st.subheader(f"County comparison – Inclusive Growth ({latest_year})")
        st.bar_chart(comparison_df)

    # --- Quick stats --------------------------------------------------
    st.subheader("Quick stats")

    if not filtered_df.empty:
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Average Inclusive Growth Score",
            f"{filtered_df['inclusive_growth_score'].mean():.1f}",
        )
        col2.metric(
            "Average Affordable Housing Score",
            f"{filtered_df['affordable_housing_score'].mean():.1f}",
        )
        col3.metric(
            "Average Internet Access Score",
            f"{filtered_df['internet_access_score'].mean():.1f}",
        )
    else:
        st.write("No data available for this selection.")

    # --- Download CSV button ------------------------------------------
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data as CSV",
        data=csv_bytes,
        file_name=(
            f"{county.replace(' ', '_').lower()}_{year_filter}_metrics.csv"
            if year_filter != "All"
            else f"{county.replace(' ', '_').lower()}_all_years_metrics.csv"
        ),
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
