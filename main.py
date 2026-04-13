"""
Main entry point for the stock pipeline application
Demonstrates how to use the complete pipeline
"""
import asyncio
import logging
from config.settings import Config, LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Main application entry point"""
    logger.info("Starting Stock Pipeline Application...")

    from src.database import init_db, close_db
    from src.api_clients import fetch_multiple_quotes
    from src.processors import process_stock_quote
    from src.database import get_db, get_stock_by_symbol, create_stock
    from src.database.crud import create_stock_price

    try:
        # 1. Initialize database
        logger.info("Step 1: Initializing database...")
        await init_db()

        # 2. Example: Fetch data from APIs
        logger.info("Step 2: Fetching stock data from API...")
        symbols = ["AAPL", "GOOGL", "MSFT"]
        quotes = await fetch_multiple_quotes(symbols)

        # 3. Process and store data
        logger.info("Step 3: Processing and storing data...")
        async with get_db() as session:
            for symbol, raw_quote in quotes.items():
                if raw_quote is None:
                    logger.warning(f"Skipping {symbol} - no data")
                    continue

                try:
                    # Process API data
                    validated_quote = await process_stock_quote(raw_quote)

                    # Check if stock exists, create if not
                    stock = await get_stock_by_symbol(session, symbol)
                    if not stock:
                        stock = await create_stock(session, symbol)

                    # Save price data
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
                    logger.info(f"Saved {symbol}: ${price.price}")

                except Exception as e:
                    logger.error(f"Error processing {symbol}: {e}")

        # 4. Information about running the REST server
        logger.info("\n" + "="*60)
        logger.info("Stock Pipeline Application Ready!")
        logger.info("="*60)
        logger.info("\nTo start the REST API server, run:")
        logger.info(f"  uvicorn src.server.app:app --host {Config.server_host} --port {Config.server_port} --reload")
        logger.info("\nAPI Documentation will be available at:")
        logger.info(f"  http://localhost:{Config.server_port}/docs")
        logger.info("\nAvailable endpoints:")
        logger.info("  POST   /stocks                                  - Create a new stock")
        logger.info("  GET    /stocks                                  - List all stocks")
        logger.info("  GET    /stocks/{stock_id}                       - Get stock details")
        logger.info("  PUT    /stocks/{stock_id}                       - Update stock")
        logger.info("  DELETE /stocks/{stock_id}                       - Delete stock")
        logger.info("  GET    /stocks/symbol/{symbol}/latest           - Get latest price")
        logger.info("  GET    /stocks/symbol/{symbol}/prices           - Get all prices")
        logger.info("  GET    /stocks/symbol/{symbol}/stats            - Get statistics")
        logger.info("  POST   /fetch/quote/{symbol}                    - Fetch from API")
        logger.info("  POST   /fetch/quotes?symbols=AAPL&symbols=GOOGL - Fetch multiple")
        logger.info("\n" + "="*60)

        logger.info("Application started successfully")

    except Exception as e:
        logger.error(f"Error in main application: {e}", exc_info=True)
        raise

    finally:
        logger.info("Closing database connection...")
        await close_db()


if __name__ == "__main__":
    asyncio.run(main())
