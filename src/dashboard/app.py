import streamlit as st
import sys
from pathlib import Path
import calendar

ROOT_DIR = (str(Path(__file__).resolve().parents[2]))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.dashboard.api_client import fetch_endpoint
from src.dashboard.charts import (
    build_annual_comparison_chart,
    build_monthly_evolution_chart,
    build_seller_ranking_chart
)

st.set_page_config(
    page_title="Energy Budget Analytics",
    page_icon=" ⚡ ",
    layout="wide"
)

st.title("Energy Budget Analytics - Commercial Dashboard")
st.markdown("Monitoring annual targets, monthly progression, and sales team performance")

df_annual = fetch_endpoint("/targets/annual")
df_monthly = fetch_endpoint("/targets/monthly")
df_sellers = fetch_endpoint("/performance/sellers")

if df_annual.empty or df_monthly.empty or df_sellers.empty:
    st.warning("API unavailable or no data found. Start the backend with `uvicorn src.api.main:app --Start the backend with `uvicorn src.api.main:app --reload`.reload`")
    st.stop()

st.sidebar.header("Filters")
categories = sorted(df_annual["category"].unique().tolist())
selected_category = st.sidebar.selectbox(
    "Category",
    options=["All"] + categories
)

months = sorted(df_monthly["month_number"].unique().tolist())
selected_month = st.sidebar.selectbox(
    "Month",
    options=["All"] + months,
    format_func=lambda m: "All months" if m == "All" else calendar.month_name[int(m)]
)

filtered_annual = (
    df_annual if selected_category == "All" else df_annual[df_annual["category"] == selected_category]
)

filtered_monthly = (
    df_monthly if selected_category == "All" else df_monthly[df_monthly["category"] == selected_category]
)

filtered_sellers = (
    df_sellers if selected_month == "All" else df_sellers[df_sellers["month_number"] == selected_month]
)

total_predicted = float(filtered_annual["predicted_total_year"].sum())
total_realized = float(filtered_annual["realized_total_year"].sum())
overall_completion = (total_realized / total_predicted * 100) if total_predicted > 0 else 0.0

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Annual Predicted Target", f"R$ {total_predicted:,.2f}")
kpi2.metric("Total Realized", f"R$ {total_realized:,.2f}")
kpi3.metric("Consolidated Completion", f"{overall_completion: .1f}%")

st.divider()

col1,col2 = st.columns(2)
with col1:
    st.subheader("Predicted vs. Realized by Category (Annual)")
    st.plotly_chart(build_annual_comparison_chart(filtered_annual), use_container_width=True)
with col2:
    st.subheader("Monthly Progression (Predicted vs. Realized)")
    st.plotly_chart(build_monthly_evolution_chart(filtered_monthly), use_container_width=True)

st.divider()

st.subheader("Sales Team Performance (% Target Achieved)")
st.plotly_chart(build_seller_ranking_chart(filtered_sellers), use_container_width=True)