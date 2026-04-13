"""
Pydantic schemas for data validation
Used for API requests/responses and data validation
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class StockPriceCreate(BaseModel):
    """Schema for creating a new stock price record"""
    symbol: str = Field(..., min_length=1, max_length=10, description="Stock symbol (e.g., AAPL)")
    price: float = Field(..., gt=0, description="Current price")
    open_price: Optional[float] = Field(None, gt=0, description="Opening price")
    high_price: Optional[float] = Field(None, gt=0, description="Highest price")
    low_price: Optional[float] = Field(None, gt=0, description="Lowest price")
    volume: Optional[int] = Field(None, ge=0, description="Trading volume")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Price timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "price": 150.50,
                "open_price": 149.00,
                "high_price": 151.00,
                "low_price": 148.50,
                "volume": 5000000,
                "timestamp": "2026-04-13T10:30:00"
            }
        }


class StockPriceResponse(BaseModel):
    """Schema for stock price response from API"""
    id: int
    stock_id: int
    price: float
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    volume: Optional[int] = None
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True  # Allow conversion from ORM objects


class StockCreate(BaseModel):
    """Schema for creating a new stock"""
    symbol: str = Field(..., min_length=1, max_length=10, description="Stock symbol")
    company_name: Optional[str] = Field(None, max_length=255, description="Company name")
    sector: Optional[str] = Field(None, max_length=100, description="Sector/industry")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "company_name": "Apple Inc.",
                "sector": "Technology"
            }
        }


class StockResponse(BaseModel):
    """Schema for stock response (without prices)"""
    id: int
    symbol: str
    company_name: Optional[str] = None
    sector: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StockDetailResponse(StockResponse):
    """Schema for detailed stock response (includes prices)"""
    prices: List[StockPriceResponse] = []

    class Config:
        from_attributes = True


class StockPriceListResponse(BaseModel):
    """Schema for listing stock prices"""
    symbol: str
    current_price: float
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    volume: Optional[int] = None
    timestamp: datetime
    count: int = Field(default=1, description="Number of price records for this symbol")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "current_price": 150.50,
                "high_price": 151.00,
                "low_price": 148.50,
                "volume": 5000000,
                "timestamp": "2026-04-13T10:30:00",
                "count": 1
            }
        }
