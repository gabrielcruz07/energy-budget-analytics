from pydantic import BaseModel, ConfigDict

class AnnualTargetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_id: int
    category: str
    predicted_total_year: float
    realized_total_year: float
    completion_percentage: float

class MonthlyTargetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_id: int
    category: str
    month_name: str
    month_number: int
    predicted_month: float
    realized_month: float
    completion_percentage: float

class SellerPerformanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_id: int
    seller_name: str
    month_name: str
    month_number: int
    completion_percentage: float
