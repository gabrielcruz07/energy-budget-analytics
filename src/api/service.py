from typing import Optional
from sqlalchemy import create_engine, text

from src.config import DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def _run(query: str, params: dict):
    with engine.connect() as conn:
        return conn.execute(text(query), params).mappings().all()


def fetch_annual_targets(category: Optional[str] = None):
    query = """
        SELECT source_id, category, predicted_total_year, realized_total_year, completion_percentage
        FROM annual_targets
    """
    params = {}

    if category:
        query += " WHERE LOWER(category) = LOWER(:category)"
        params["category"] = category

    query += " ORDER BY category ASC"
    return _run(query, params)


def fetch_monthly_targets(category: Optional[str] = None,
                          month_number: Optional[int] = None):
    query = """
        SELECT source_id, category, month_name, month_number,
               predicted_month, realized_month, completion_percentage
        FROM monthly_targets
        WHERE 1=1
    """
    params = {}

    if category:
        query += " AND LOWER(category) = LOWER(:category)"
        params["category"] = category
    if month_number:
        query += " AND month_number = :month_number"
        params["month_number"] = month_number

    query += " ORDER BY month_number ASC, category ASC"
    return _run(query, params)


def fetch_seller_performance(seller_name: Optional[str] = None,
                             month_number: Optional[int] = None):
    query = """
        SELECT source_id, seller_name, month_name, month_number, completion_percentage
        FROM seller_performance
        WHERE 1=1
    """
    params = {}

    if seller_name:
        query += " AND LOWER(seller_name) = LOWER(:seller_name)"
        params["seller_name"] = seller_name
    if month_number:
        query += " AND month_number = :month_number"
        params["month_number"] = month_number

    query += " ORDER BY month_number ASC, completion_percentage DESC"
    return _run(query, params)
