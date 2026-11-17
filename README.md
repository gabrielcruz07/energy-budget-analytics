# ⚡ Energy Budget Analytics Pipeline (WIP)

**Status:** 🚧 Work in Progress (Phase 2: Database Ingestion & API Layer)

## 📌 Business Objective
End-to-end Data Engineering pipeline designed to extract legacy commercial spreadsheets (with localized currency and percentage strings), clean and standardize the schema into English `snake_case`, load the structured data into a cloud PostgreSQL database, and expose business metrics via a RESTful API.

## 🏗️ Architecture (Monorepo)
- **`data/`**: Raw legacy CSV files (Excluded via `.gitignore`).
- **`notebooks/`**: Jupyter environment for mock data generation and ETL prototyping.
- **`src/etl/`**: Production Python scripts for automated data cleaning and database ingestion.
- **`src/api/`**: FastAPI backend with Pydantic validation to serve commercial metrics.

## 🛠️ Tech Stack
- **Data Engineering:** Python, Pandas, SQLAlchemy, Psycopg2
- **Database:** PostgreSQL (Cloud / Neon.tech)
- **Backend & API:** FastAPI, Pydantic, Uvicorn
- **Environment:** Conda

## 🚀 Current Progress
- [x] Synthetic legacy data generator implemented (`00_generate_mock_data.ipynb`).
- [x] Data cleaning, currency/percentage parsing, and schema mapping validated (`01_etl_prototyping.ipynb`).
- [x] Cloud PostgreSQL provisioning & automated ingestion (`src/etl/pipeline.py`).
- [ ] FastAPI endpoints development (`src/api/main.py`) and cloud deployment.
