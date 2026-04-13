"""
CRUD operations for database models
Create, Read, Update, Delete operations with async/await
"""
import logging
from datetime import datetime, timedelta
from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Stock, StockPrice

logger = logging.getLogger(__name__)


# ==================== STOCK OPERATIONS ====================

async def create_stock(
    session: AsyncSession,
    symbol: str,
    company_name: str = None,
    sector: str = None,
) -> Stock:
    """
    Create a new stock record

    Args:
        session: Database session
        symbol: Stock symbol (AAPL, GOOGL, etc.)
        company_name: Company name
        sector: Industry/sector

    Returns:
        Created Stock object
    """
    stock = Stock(
        symbol=symbol,
        company_name=company_name,
        sector=sector,
    )
    session.add(stock)
    await session.flush()  # Get the ID without committing
    logger.info(f"Created stock: {symbol}")
    return stock


async def get_stock_by_symbol(session: AsyncSession, symbol: str) -> Stock | None:
    """
    Get stock by symbol

    Args:
        session: Database session
        symbol: Stock symbol

    Returns:
        Stock object or None if not found
    """
    result = await session.execute(
        select(Stock).where(Stock.symbol == symbol)
    )
    return result.scalars().first()


async def get_stock_by_id(session: AsyncSession, stock_id: int) -> Stock | None:
    """
    Get stock by ID

    Args:
        session: Database session
        stock_id: Stock ID

    Returns:
        Stock object or None if not found
    """
    result = await session.execute(
        select(Stock).where(Stock.id == stock_id)
    )
    return result.scalars().first()


async def get_all_stocks(session: AsyncSession, skip: int = 0, limit: int = 10) -> list[Stock]:
    """
    Get all stocks with pagination

    Args:
        session: Database session
        skip: Number of records to skip
        limit: Number of records to return

    Returns:
        List of Stock objects
    """
    result = await session.execute(
        select(Stock).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def update_stock(
    session: AsyncSession,
    stock_id: int,
    company_name: str = None,
    sector: str = None,
) -> Stock | None:
    """
    Update a stock record

    Args:
        session: Database session
        stock_id: Stock ID to update
        company_name: New company name
        sector: New sector

    Returns:
        Updated Stock object or None if not found
    """
    stock = await get_stock_by_id(session, stock_id)
    if not stock:
        return None

    if company_name:
        stock.company_name = company_name
    if sector:
        stock.sector = sector

    stock.updated_at = datetime.utcnow()
    await session.flush()
    logger.info(f"Updated stock: {stock.symbol}")
    return stock


async def delete_stock(session: AsyncSession, stock_id: int) -> bool:
    """
    Delete a stock record

    Args:
        session: Database session
        stock_id: Stock ID to delete

    Returns:
        True if deleted, False if not found
    """
    stock = await get_stock_by_id(session, stock_id)
    if not stock:
        return False

    await session.delete(stock)
    await session.flush()
    logger.info(f"Deleted stock: {stock.symbol}")
    return True


# ==================== STOCK PRICE OPERATIONS ====================

async def create_stock_price(
    session: AsyncSession,
    stock_id: int,
    price: float,
    open_price: float = None,
    high_price: float = None,
    low_price: float = None,
    volume: int = None,
    timestamp: datetime = None,
) -> StockPrice:
    """
    Create a new stock price record

    Args:
        session: Database session
        stock_id: Stock ID (foreign key)
        price: Current price
        open_price: Opening price
        high_price: Highest price
        low_price: Lowest price
        volume: Trading volume
        timestamp: Price timestamp

    Returns:
        Created StockPrice object
    """
    if timestamp is None:
        timestamp = datetime.utcnow()

    stock_price = StockPrice(
        stock_id=stock_id,
        price=price,
        open_price=open_price,
        high_price=high_price,
        low_price=low_price,
        volume=volume,
        timestamp=timestamp,
    )
    session.add(stock_price)
    await session.flush()
    return stock_price


async def get_latest_price(session: AsyncSession, stock_id: int) -> StockPrice | None:
    """
    Get the latest price record for a stock

    Args:
        session: Database session
        stock_id: Stock ID

    Returns:
        Latest StockPrice object or None if not found
    """
    result = await session.execute(
        select(StockPrice)
        .where(StockPrice.stock_id == stock_id)
        .order_by(desc(StockPrice.timestamp))
        .limit(1)
    )
    return result.scalars().first()


async def get_prices_by_symbol(
    session: AsyncSession,
    symbol: str,
    skip: int = 0,
    limit: int = 100,
) -> list[StockPrice]:
    """
    Get all prices for a stock by symbol

    Args:
        session: Database session
        symbol: Stock symbol
        skip: Number of records to skip
        limit: Number of records to return

    Returns:
        List of StockPrice objects
    """
    result = await session.execute(
        select(StockPrice)
        .join(Stock)
        .where(Stock.symbol == symbol)
        .order_by(desc(StockPrice.timestamp))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_prices_by_date_range(
    session: AsyncSession,
    stock_id: int,
    start_date: datetime,
    end_date: datetime,
) -> list[StockPrice]:
    """
    Get prices within a date range

    Args:
        session: Database session
        stock_id: Stock ID
        start_date: Start date
        end_date: End date

    Returns:
        List of StockPrice objects
    """
    result = await session.execute(
        select(StockPrice)
        .where(
            and_(
                StockPrice.stock_id == stock_id,
                StockPrice.timestamp >= start_date,
                StockPrice.timestamp <= end_date,
            )
        )
        .order_by(StockPrice.timestamp)
    )
    return result.scalars().all()


async def get_stock_price_stats(
    session: AsyncSession,
    stock_id: int,
    days: int = 30,
) -> dict:
    """
    Get price statistics for a stock (high, low, avg) for last N days

    Args:
        session: Database session
        stock_id: Stock ID
        days: Number of days to look back

    Returns:
        Dictionary with stats (high, low, avg, count)
    """
    start_date = datetime.utcnow() - timedelta(days=days)

    prices = await get_prices_by_date_range(
        session, stock_id, start_date, datetime.utcnow()
    )

    if not prices:
        return {"high": None, "low": None, "avg": None, "count": 0}

    price_values = [p.price for p in prices]
    return {
        "high": max(price_values),
        "low": min(price_values),
        "avg": sum(price_values) / len(price_values),
        "count": len(prices),
    }


async def delete_old_prices(
    session: AsyncSession,
    days: int = 90,
) -> int:
    """
    Delete price records older than N days
    Helps keep database clean

    Args:
        session: Database session
        days: Delete records older than this many days

    Returns:
        Number of records deleted
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    result = await session.execute(
        select(StockPrice).where(StockPrice.created_at < cutoff_date)
    )
    old_prices = result.scalars().all()

    for price in old_prices:
        await session.delete(price)

    await session.flush()
    logger.info(f"Deleted {len(old_prices)} old price records")
    return len(old_prices)
