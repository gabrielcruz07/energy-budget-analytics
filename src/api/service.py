from typing import Optional
from sqlalchemy import create_engine, text

from src.config import DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")

engine = create_engine(DATABASE_URL)

def fetch_annual_targets(category: Optional[str] = None):
    query = """
            SELECT source_id, category, predicted_total_year, realized_total_year, completion_percentage
            FROM annual_targets
    """

    query_params = {}

    if category:
        query += "WHERE LOWER(category) = LOWER(:filter)"
        query_params["filter"] = category

    with engine.connect() as conn:
        return conn.execute(text(query), query_params).mappings().all()

def fetch_monthly_targets(category: Optional[str] = None,
                          month_number: Optional[int] = None):
    query = """
            SELECT source_id, category, month_name, month_number, predicted_total_month, realized_total_month, completion_percentage
            FROM monthly_targets
            WHERE 1=1
    """
    query_params = {}

    if category:
        query += "AND LOWER(category) = LOWER(:filter)"
        query_params["filter"] = category
    if month_number:
        query += "AND LOWER(month_number) = :month_number"
        query_params["month_number"] = month_number

    query += "ORDER BY month_name ASC"

def fetch_seller_performance(
        seller_name: Optional[str] = None,
        month_number: Optional[int] = None
):
    query = """
            SELECT source_id, seller_name, month_name, month_number, completion_percentage
            FROM seller_performance
            WHERE 1=1
    """
    query_params = {}

    if seller_name:
        query += "AND LOWER(seller_name) = :seller_name"
        query_params["seller_name"] = seller_name
    if month_number:
        query += "AND LOWER(month_number) = :month_number"
        query_params["month_number"] = month_number

    query += "ORDER BY month_name ASC, completion_percentage DESC"

    with engine.connect() as conn:
        return conn.execute(text(query), query_params).mappings().all()