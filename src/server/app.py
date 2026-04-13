"""
FastAPI application for Stock Pipeline REST API
"""
import logging
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import (
    get_db,
    init_db,
    close_db,
    get_stock_by_symbol,
    get_stock_by_id,
    get_all_stocks,
    create_stock,
    update_stock,
    delete_stock,
    get_latest_price,
    get_prices_by_symbol,
    get_stock_price_stats,
)
from src.models.schemas import (
    StockCreate,
    StockResponse,
    StockDetailResponse,
    StockPriceCreate,
    StockPriceResponse,
    StockPriceListResponse,
)
from src.api_clients import fetch_stock_quote, fetch_multiple_quotes
from src.processors import process_stock_quote, process_company_info

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Stock Pipeline API",
    description="Real-time stock data pipeline with async processing",
    version="0.1.0",
)


# ==================== STARTUP / SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Starting Stock Pipeline API...")
    await init_db()
    logger.info("Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    logger.info("Shutting down Stock Pipeline API...")
    await close_db()
    logger.info("API shutdown complete")


# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "stock-pipeline"}


# ==================== STOCK ENDPOINTS ====================

@app.post("/stocks", response_model=StockResponse)
async def create_new_stock(stock_data: StockCreate):
    """
    Create a new stock

    Args:
        stock_data: Stock information (symbol, company_name, sector)

    Returns:
        Created stock with ID
    """
    try:
        async with get_db() as session:
            # Check if stock already exists
            existing = await get_stock_by_symbol(session, stock_data.symbol)
            if existing:
                raise HTTPException(
                    status_code=409,
                    detail=f"Stock {stock_data.symbol} already exists"
                )

            # Create new stock
            stock = await create_stock(
                session,
                symbol=stock_data.symbol,
                company_name=stock_data.company_name,
                sector=stock_data.sector,
            )
            return StockResponse.from_orm(stock)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating stock: {e}")
        raise HTTPException(status_code=500, detail="Failed to create stock")


@app.get("/stocks/{stock_id}", response_model=StockDetailResponse)
async def get_stock_detail(stock_id: int):
    """
    Get stock details with all prices

    Args:
        stock_id: Stock ID

    Returns:
        Stock with prices
    """
    try:
        async with get_db() as session:
            stock = await get_stock_by_id(session, stock_id)

            if not stock:
                raise HTTPException(
                    status_code=404,
                    detail=f"Stock with ID {stock_id} not found"
                )

            return StockDetailResponse.from_orm(stock)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching stock: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch stock")


@app.get("/stocks", response_model=list[StockResponse])
async def list_stocks(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """
    List all stocks with pagination

    Args:
        skip: Number of records to skip
        limit: Number of records to return (max 100)

    Returns:
        List of stocks
    """
    try:
        async with get_db() as session:
            stocks = await get_all_stocks(session, skip=skip, limit=limit)
            return [StockResponse.from_orm(stock) for stock in stocks]

    except Exception as e:
        logger.error(f"Error listing stocks: {e}")
        raise HTTPException(status_code=500, detail="Failed to list stocks")


@app.put("/stocks/{stock_id}", response_model=StockResponse)
async def update_stock_info(
    stock_id: int,
    stock_data: StockCreate,
):
    """
    Update stock information

    Args:
        stock_id: Stock ID to update
        stock_data: Updated stock data

    Returns:
        Updated stock
    """
    try:
        async with get_db() as session:
            stock = await update_stock(
                session,
                stock_id=stock_id,
                company_name=stock_data.company_name,
                sector=stock_data.sector,
            )

            if not stock:
                raise HTTPException(
                    status_code=404,
                    detail=f"Stock with ID {stock_id} not found"
                )

            return StockResponse.from_orm(stock)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating stock: {e}")
        raise HTTPException(status_code=500, detail="Failed to update stock")


@app.delete("/stocks/{stock_id}")
async def delete_stock_endpoint(stock_id: int):
    """
    Delete a stock

    Args:
        stock_id: Stock ID to delete

    Returns:
        Success message
    """
    try:
        async with get_db() as session:
            deleted = await delete_stock(session, stock_id)

            if not deleted:
                raise HTTPException(
                    status_code=404,
                    detail=f"Stock with ID {stock_id} not found"
                )

            return {"message": "Stock deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting stock: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete stock")


# ==================== PRICE ENDPOINTS ====================

@app.get("/stocks/symbol/{symbol}/latest", response_model=StockPriceResponse)
async def get_latest_stock_price(symbol: str):
    """
    Get latest price for a stock

    Args:
        symbol: Stock symbol (AAPL, GOOGL, etc.)

    Returns:
        Latest price record
    """
    try:
        async with get_db() as session:
            stock = await get_stock_by_symbol(session, symbol)

            if not stock:
                raise HTTPException(
                    status_code=404,
                    detail=f"Stock {symbol} not found"
                )

            price = await get_latest_price(session, stock.id)

            if not price:
                raise HTTPException(
                    status_code=404,
                    detail=f"No prices found for {symbol}"
                )

            return StockPriceResponse.from_orm(price)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching price: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch price")


@app.get("/stocks/symbol/{symbol}/prices", response_model=list[StockPriceResponse])
async def get_stock_prices(
    symbol: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(30, ge=1, le=100),
):
    """
    Get all prices for a stock

    Args:
        symbol: Stock symbol
        skip: Number of records to skip
        limit: Number of records to return

    Returns:
        List of price records
    """
    try:
        async with get_db() as session:
            prices = await get_prices_by_symbol(session, symbol, skip=skip, limit=limit)

            if not prices:
                raise HTTPException(
                    status_code=404,
                    detail=f"No prices found for {symbol}"
                )

            return [StockPriceResponse.from_orm(price) for price in prices]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching prices: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch prices")


@app.get("/stocks/symbol/{symbol}/stats")
async def get_stock_statistics(
    symbol: str,
    days: int = Query(30, ge=1, le=365),
):
    """
    Get price statistics for a stock

    Args:
        symbol: Stock symbol
        days: Number of days to analyze (default 30)

    Returns:
        Statistics (high, low, avg, count)
    """
    try:
        async with get_db() as session:
            stock = await get_stock_by_symbol(session, symbol)

            if not stock:
                raise HTTPException(
                    status_code=404,
                    detail=f"Stock {symbol} not found"
                )

            stats = await get_stock_price_stats(session, stock.id, days=days)

            if stats["count"] == 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"No price data found for {symbol} in last {days} days"
                )

            return {
                "symbol": symbol,
                "period_days": days,
                **stats,
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")


# ==================== FETCH FROM API ENDPOINTS ====================

@app.post("/fetch/quote/{symbol}")
async def fetch_and_save_quote(symbol: str):
    """
    Fetch latest quote from Alpha Vantage API and save to database

    Args:
        symbol: Stock symbol

    Returns:
        Saved price data
    """
    try:
        # Fetch from API
        raw_quote = await fetch_stock_quote(symbol)

        # Process data
        validated_quote = await process_stock_quote(raw_quote)

        # Save to database
        async with get_db() as session:
            # Ensure stock exists
            stock = await get_stock_by_symbol(session, validated_quote.symbol)
            if not stock:
                stock = await create_stock(session, validated_quote.symbol)

            # Import create_stock_price here to avoid circular import
            from src.database.crud import create_stock_price
            price = await create_stock_price(
                session,
                stock_id=stock.id,
                price=validated_quote.price,
                open_price=validated_quote.open_price,
                high_price=validated_quote.high_price,
                low_price=validated_quote.low_price,
                volume=validated_quote.volume,
                timestamp=validated_quote.timestamp,
            )

            return StockPriceResponse.from_orm(price)

    except Exception as e:
        logger.error(f"Error fetching and saving quote: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch quote: {str(e)}")


@app.post("/fetch/quotes")
async def fetch_and_save_multiple_quotes(symbols: list[str] = Query(...)):
    """
    Fetch quotes for multiple stocks concurrently

    Args:
        symbols: List of stock symbols

    Returns:
        Dictionary with symbol -> price mapping
    """
    try:
        # Fetch from API
        raw_quotes = await fetch_multiple_quotes(symbols)

        results = {}

        # Process and save each quote
        async with get_db() as session:
            from src.database.crud import create_stock_price

            for symbol, raw_quote in raw_quotes.items():
                if raw_quote is None:
                    results[symbol] = {"error": "Failed to fetch"}
                    continue

                try:
                    # Process data
                    validated_quote = await process_stock_quote(raw_quote)

                    # Ensure stock exists
                    stock = await get_stock_by_symbol(session, validated_quote.symbol)
                    if not stock:
                        stock = await create_stock(session, validated_quote.symbol)

                    # Save price
                    price = await create_stock_price(
                        session,
                        stock_id=stock.id,
                        price=validated_quote.price,
                        open_price=validated_quote.open_price,
                        high_price=validated_quote.high_price,
                        low_price=validated_quote.low_price,
                        volume=validated_quote.volume,
                        timestamp=validated_quote.timestamp,
                    )

                    results[symbol] = StockPriceResponse.from_orm(price).dict()

                except Exception as e:
                    logger.error(f"Error processing {symbol}: {e}")
                    results[symbol] = {"error": str(e)}

        return results

    except Exception as e:
        logger.error(f"Error fetching multiple quotes: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch quotes: {str(e)}")
