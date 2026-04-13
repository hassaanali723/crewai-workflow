"""
SQLAlchemy ORM models for database tables
Defines Stock and StockPrice entities with relationships
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database.connection import Base


class Stock(Base):
    """
    Represents a stock symbol (e.g., AAPL, GOOGL, MSFT)
    One Stock can have many StockPrice records
    """
    __tablename__ = "stocks"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Stock symbol (AAPL, GOOGL, etc.)
    symbol = Column(String(10), unique=True, nullable=False, index=True)

    # Company name
    company_name = Column(String(255))

    # Sector/industry
    sector = Column(String(100))

    # When this record was created
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # When this record was last updated
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship: One Stock has many StockPrices
    prices = relationship(
        "StockPrice",
        back_populates="stock",
        cascade="all, delete-orphan",  # Delete prices when stock is deleted
        lazy="select"
    )

    def __repr__(self):
        return f"<Stock(id={self.id}, symbol={self.symbol}, company={self.company_name})>"


class StockPrice(Base):
    """
    Represents historical/current price data for a stock
    Many StockPrice records belong to one Stock
    """
    __tablename__ = "stock_prices"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to Stock table
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False, index=True)

    # Current price
    price = Column(Float, nullable=False)

    # Opening price for the day
    open_price = Column(Float)

    # Highest price for the day
    high_price = Column(Float)

    # Lowest price for the day
    low_price = Column(Float)

    # Trading volume
    volume = Column(Integer)

    # Timestamp of the price data
    timestamp = Column(DateTime, nullable=False, index=True)

    # When this record was created in our database
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship: Many StockPrices belong to one Stock
    stock = relationship(
        "Stock",
        back_populates="prices",
        lazy="select"
    )

    def __repr__(self):
        return f"<StockPrice(stock_id={self.stock_id}, price={self.price}, timestamp={self.timestamp})>"
