import pandas as pd
import requests
import streamlit as st
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.config import API_URL


def _get_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_endpoint(endpoint: str, params: dict | None = None) -> pd.DataFrame:
    session = _get_session()
    try:
        response = session.get(f"{API_URL}{endpoint}", params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data) if data else pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.warning(f"Fail to verify {endpoint} at API ({API_URL}): {e}")
        return pd.DataFrame()