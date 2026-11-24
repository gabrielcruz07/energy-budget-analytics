from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
import src.api.service as service

from src.api.schemas import (
    AnnualTargetResponse,
    MonthlyTargetResponse,
    SellerPerformanceResponse
)

app = FastAPI(
    title="Energy Budget Analytics API",
    description="REST API serving cleaned commercial targets and seller performance metrics from PostgreSQL",
    version="1.0",
)

@app.get("/",tags =["Health"])
def health_check():
    return{
        "status": "online",
        "service":"Energy Budget Analytics API",
        "docs_url":"/docs"
    }

@app.get("/targets/annual",response_model=AnnualTargetResponse,tags=["annual"])
def get_annual_targets(
    category: Optional[str] = Query(None, description="Filter by category name")
):
    result = service.fetch_annual_targets(category=category)
    if not result:
        raise HTTPException(status_code=404, detail="No annual targets found")
    return result

@app.get("/targets/monthly",response_model=MonthlyTargetResponse,tags=["monthly"])
def get_monthly_targets(
        category: Optional[str] = Query(None, description="Filter by category name"),
        month_number: Optional[int] = Query(None, ge=1, le=12, description="Filter by month number")
):
    result = service.fetch_monthly_targets(category=category, month_number=month_number)
    if not result:
        raise HTTPException(status_code=404, detail="No monthly targets found")
    return result

@app.get("/performance/sellers",response_model=SellerPerformanceResponse,tags=["sellers"])
def get_seller_performance(
        seller_name: Optional[str] = Query(None, description="Filter by seller name"),
        month_number: Optional[int] = Query(None, description="Filter by month number")
):
    result = service.fetch_seller_performance(seller_name=seller_name, month_number=month_number)
    if not result:
        raise HTTPException(status_code=404, detail="No sellers found")
    return result


