# Marks src.frontend as a package (can be empty).
import requests
import pandas as pd
import streamlit as st

API_URL = "http://localhost:8000"  # FastAPI base URL


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

    # ----- Summary line chart -----
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

    # ----- Tract-level table -----
    st.subheader(f"Census Tract Detail – {county}")
    county_data = get_county_metrics(county, year_value)
    tracts_df = pd.DataFrame(county_data["rows"])

    if year_value is not None:
        st.caption(f"Showing census tracts for **{county}**, year **{year_value}**.")
    else:
        st.caption(f"Showing all years for **{county}** (sorted by year and tract).")

    st.dataframe(tracts_df, use_container_width=True)

    # Simple summary stats
    st.subheader("Quick stats")
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Inclusive Growth Score",
        f"{tracts_df['inclusive_growth_score'].mean():.1f}",
    )
    col2.metric(
        "Average Affordable Housing Score",
        f"{tracts_df['affordable_housing_score'].mean():.1f}",
    )
    col3.metric(
        "Average Internet Access Score",
        f"{tracts_df['internet_access_score'].mean():.1f}",
    )


if __name__ == "__main__":
    main()
