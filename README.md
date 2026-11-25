# ⚡ Energy Budget Analytics Pipeline

**Status:** ✅ Completed (v1.0) — Deployed & Live

## 🌐 Live Demo
- **Interactive Dashboard (Streamlit):** [Access Commercial Dashboard](https://energy-budget-analytics.streamlit.app)
- **REST API & Swagger Docs (FastAPI):** [Explore API Endpoints](https://energy-budget-analytics.onrender.com/docs)

> *Note: The backend API is hosted on Render's free tier and spins down after periods of inactivity. Please allow ~30–50 seconds for the initial request to wake up the server.*

## 📌 Business Objective
End-to-end Data Engineering and Business Intelligence pipeline designed to extract legacy commercial spreadsheets (with localized currency and percentage strings), clean and standardize the schema into English `snake_case`, load the structured data into a cloud PostgreSQL database, expose business metrics via a RESTful API, and deliver interactive visualizations through a BI dashboard.

## 🏗️ Architecture (Monorepo)
- **`data/`**: Raw legacy CSV files (Excluded via `.gitignore`).
- **`notebooks/`**: Jupyter environment for mock data generation and ETL prototyping.
- **`src/config.py`**: Centralized environment variables (`DATABASE_URL`, `API_URL`) and dynamic root path resolution.
- **`src/etl/`**: Production Python scripts (`pipeline.py`) for automated data cleaning and idempotent database ingestion.
- **`src/api/`**: FastAPI backend (`main.py`, `service.py`, `schemas.py`) with Pydantic validation and parameterized SQL queries to serve commercial metrics.
- **`src/dashboard/`**: Streamlit & Plotly frontend (`app.py`, `charts.py`, `api_client.py`) with cached HTTP requests, sidebar filters, and KPI cards.

## 🛠️ Tech Stack
- **Data Engineering & ETL:** Python, Pandas, SQLAlchemy, Psycopg2, Python-Dotenv
- **Database:** PostgreSQL (Cloud / Neon.tech)
- **Backend & API:** FastAPI, Pydantic, Uvicorn
- **Frontend & Visualization:** Streamlit, Plotly Express, Requests
- **Environment & Deployment:** Conda, Render (API), Streamlit Community Cloud (Dashboard)

## 🔌 API Endpoints
| Method | Endpoint | Query Parameters | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/targets/annual` | `category` *(optional)* | Annual predicted vs. realized totals and completion percentage. |
| `GET` | `/targets/monthly` | `category`, `month_number` *(optional)* | Monthly progression ordered chronologically. |
| `GET` | `/performance/sellers` | `seller_name`, `month_number` *(optional)* | Individual sales representative target completion rates. |

## 🚀 Completed Milestones (v1.0)
- [x] Synthetic legacy data generator implemented (`00_generate_mock_data.ipynb`).
- [x] Data cleaning, currency/percentage parsing, and schema mapping validated (`01_etl_prototyping.ipynb`).
- [x] Cloud PostgreSQL provisioning & automated idempotent ingestion (`src/etl/pipeline.py`).
- [x] FastAPI endpoints development with parameterized SQL & Pydantic validation (`src/api/`).
- [x] Interactive Streamlit & Plotly dashboard localized to English (`src/dashboard/`).
- [x] Cloud deployment on Neon, Render, and Streamlit Community Cloud.

## 🗺️ Roadmap (v2.0 Enhancements)
- [ ] **Executive Gauge & Composed Charts:** Upgrade Plotly visuals to mirror the original React UI (180° radial completion gauge and dual-axis Area/Bar/Line composed charts).
- [ ] **Interactive Data Grids:** Pair charts side-by-side with `st.dataframe` progress-bar columns for granular seller and client drill-down.
- [ ] **Macroeconomic Sparklines:** Integrate external currency/commodity APIs into `st.metric` sparkline cards.
- [ ] **Automated Testing & Containers:** Add `pytest` unit tests for ETL parsing functions and containerize services with Docker[cite: 3].
