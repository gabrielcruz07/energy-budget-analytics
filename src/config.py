import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def get_project_root(marker: str = "README.md") -> Path:
    current_dir = Path(__file__).resolve().parent
    for parent in [current_dir] + list(current_dir.parents):
        if(parent / marker).exists():
            return parent
    raise FileNotFoundError(f"Project root marker '{marker}' not found.")

PROJECT_ROOT = get_project_root()
DATA_DIR = PROJECT_ROOT / "data"

load_dotenv(PROJECT_ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


def _get_api_url() -> str:
    url = os.getenv("API_URL")
    if not url and "streamlit" in sys.modules:
        try:
            import streamlit as st
            url = st.secrets.get("API_URL")
        except Exception:
            url = None
    return (url or "http://127.0.0.1:8000").rstrip("/")


API_URL = _get_api_url()

