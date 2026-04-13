"""
Data Processing and Validation
Transforms API data and validates before saving to database
"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime

from src.models.schemas import StockPriceCreate, StockCreate

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Process and validate API data before saving to database
    """

    @staticmethod
    def validate_stock_quote(raw_quote: Dict[str, Any]) -> StockPriceCreate:
        """
        Validate and transform API quote to database schema

        Args:
            raw_quote: Raw data from API client (fetch_stock_quote)

        Returns:
            StockPriceCreate schema (validated by Pydantic)

        Raises:
            ValueError: If validation fails
        """
        try:
            # Extract data with fallbacks
            symbol = raw_quote.get("symbol", "").upper()
            price = float(raw_quote.get("price", 0))
            open_price = float(raw_quote.get("open_price", 0)) or None
            high_price = float(raw_quote.get("high_price", 0)) or None
            low_price = float(raw_quote.get("low_price", 0)) or None
            volume = int(raw_quote.get("volume", 0)) or None
            timestamp = raw_quote.get("timestamp", datetime.utcnow())

            # Validate with Pydantic
            validated = StockPriceCreate(
                symbol=symbol,
                price=price,
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                volume=volume,
                timestamp=timestamp,
            )

            logger.info(f"Validated quote for {symbol}: ${price}")
            return validated

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise ValueError(f"Invalid quote data: {e}")

    @staticmethod
    def validate_intraday_prices(
        raw_intraday: Dict[str, Any],
    ) -> list[StockPriceCreate]:
        """
        Validate and transform intraday time series data

        Args:
            raw_intraday: Raw data from get_intraday()

        Returns:
            List of validated StockPriceCreate objects

        Raises:
            ValueError: If validation fails
        """
        try:
            symbol = raw_intraday.get("symbol", "").upper()
            prices = raw_intraday.get("prices", [])

            validated_prices = []

            for price_data in prices:
                validated = StockPriceCreate(
                    symbol=symbol,
                    price=float(price_data.get("close", 0)),
                    open_price=float(price_data.get("open", 0)) or None,
                    high_price=float(price_data.get("high", 0)) or None,
                    low_price=float(price_data.get("low", 0)) or None,
                    volume=int(price_data.get("volume", 0)) or None,
                    timestamp=price_data.get("timestamp", datetime.utcnow()),
                )
                validated_prices.append(validated)

            logger.info(f"Validated {len(validated_prices)} intraday prices for {symbol}")
            return validated_prices

        except Exception as e:
            logger.error(f"Error validating intraday data: {e}")
            raise ValueError(f"Invalid intraday data: {e}")

    @staticmethod
    def validate_company_info(raw_company: Dict[str, Any]) -> StockCreate:
        """
        Validate and transform company information

        Args:
            raw_company: Raw data from get_company_info()

        Returns:
            StockCreate schema (validated by Pydantic)

        Raises:
            ValueError: If validation fails
        """
        try:
            symbol = raw_company.get("symbol", "").upper()
            company_name = raw_company.get("name", "")
            sector = raw_company.get("sector", "")

            # Validate with Pydantic
            validated = StockCreate(
                symbol=symbol,
                company_name=company_name or None,
                sector=sector or None,
            )

            logger.info(f"Validated company info for {symbol}: {company_name}")
            return validated

        except Exception as e:
            logger.error(f"Error validating company info: {e}")
            raise ValueError(f"Invalid company data: {e}")

    @staticmethod
    def check_data_quality(quote: StockPriceCreate) -> bool:
        """
        Perform data quality checks

        Args:
            quote: Validated quote data

        Returns:
            True if data passes quality checks

        Raises:
            ValueError: If data fails quality checks
        """
        # Check 1: Price should be positive
        if quote.price <= 0:
            raise ValueError(f"Invalid price: ${quote.price}")

        # Check 2: High should be >= low
        if quote.high_price and quote.low_price:
            if quote.high_price < quote.low_price:
                raise ValueError(
                    f"High price (${quote.high_price}) < Low price (${quote.low_price})"
                )

        # Check 3: Current price should be between high and low
        if quote.high_price and quote.low_price:
            if not (quote.low_price <= quote.price <= quote.high_price):
                logger.warning(
                    f"Price ${quote.price} outside high/low range "
                    f"({quote.low_price}-{quote.high_price})"
                )

        # Check 4: Volume should be reasonable (not negative)
        if quote.volume and quote.volume < 0:
            raise ValueError(f"Invalid volume: {quote.volume}")

        logger.debug(f"Data quality check passed for {quote.symbol}")
        return True


async def process_stock_quote(raw_quote: Dict[str, Any]) -> StockPriceCreate:
    """
    Complete processing pipeline for stock quote

    Args:
        raw_quote: Raw API response

    Returns:
        Processed and validated quote

    Raises:
        ValueError: If processing fails
    """
    # 1. Validate format
    validated = DataProcessor.validate_stock_quote(raw_quote)

    # 2. Check quality
    DataProcessor.check_data_quality(validated)

    # 3. Return processed data
    return validated


async def process_company_info(raw_company: Dict[str, Any]) -> StockCreate:
    """
    Complete processing pipeline for company info

    Args:
        raw_company: Raw API response

    Returns:
        Processed and validated company info
    """
    validated = DataProcessor.validate_company_info(raw_company)
    return validated
