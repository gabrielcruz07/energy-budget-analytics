from typing import Optional
import pandas as pd
import requests
import streamlit as st

from src.config import API_URL

st.cache_data(ttl=60)
def fetch_endpoint(endpoint: str, params: Optional[dict] = None) -> pd.DataFrame:
    """Consumes a FastAPI GET endpoint and returns a Pandas DataFrame."""
    try:
        response = requests.get(f"{API_URL}{endpoint}", params=params, timeout=10)
        response.raise_for_status()
        return pd.read_json(response.json())
    except requests.exceptions.HTTPError as exc:
        st.error(f"Fail to verify`{endpoint}` at API ({API_URL}): {exc}")
        return pd.DataFrame()