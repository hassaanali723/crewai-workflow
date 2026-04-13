"""
Alpha Vantage API Client
Async HTTP client for fetching stock data from Alpha Vantage API
"""
import asyncio
import logging
from typing import Optional, Dict, Any
import aiohttp
from datetime import datetime

from config.settings import Config

logger = logging.getLogger(__name__)


class AlphaVantageClient:
    """
    Async HTTP client for Alpha Vantage API
    Handles rate limiting, retries, and error handling
    """

    def __init__(self, api_key: str = None, timeout: int = None):
        """
        Initialize the API client

        Args:
            api_key: Alpha Vantage API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or Config.api_key
        self.base_url = Config.api_base_url
        self.timeout = timeout or Config.api_timeout
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Enter async context manager"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager"""
        if self.session:
            await self.session.close()

    async def _make_request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        retries: int = Config.max_retries,
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic

        Args:
            endpoint: API endpoint path
            params: Query parameters
            retries: Number of retries on failure

        Returns:
            JSON response data

        Raises:
            Exception: If all retries fail
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context manager")

        # Add API key to params
        params['apikey'] = self.api_key

        url = f"{self.base_url}{endpoint}"

        for attempt in range(retries):
            try:
                logger.debug(f"Request {attempt + 1}/{retries}: {endpoint}")

                async with self.session.get(
                    url,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    data = await response.json()

                    # Check for API errors
                    if "Error Message" in data:
                        raise ValueError(f"API Error: {data['Error Message']}")

                    if "Note" in data:
                        logger.warning("API Rate Limited: " + data['Note'])
                        await asyncio.sleep(Config.retry_delay * 2)
                        continue

                    logger.info(f"Successfully fetched {endpoint}")
                    return data

            except asyncio.TimeoutError:
                logger.warning(f"Request timeout (attempt {attempt + 1}/{retries})")
                if attempt < retries - 1:
                    await asyncio.sleep(Config.retry_delay)
                continue

            except aiohttp.ClientError as e:
                logger.warning(f"Network error (attempt {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(Config.retry_delay)
                continue

            except Exception as e:
                logger.error(f"Error fetching {endpoint}: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(Config.retry_delay)
                continue

        raise Exception(f"Failed to fetch {endpoint} after {retries} attempts")

    async def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get current quote for a stock symbol

        Args:
            symbol: Stock symbol (AAPL, GOOGL, etc.)

        Returns:
            Quote data with price, volume, etc.

        Example:
            >>> async with AlphaVantageClient() as client:
            ...     quote = await client.get_quote("AAPL")
            ...     print(quote)
        """
        endpoint = "/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol.upper(),
        }

        data = await self._make_request(endpoint, params)

        if "Global Quote" not in data or not data["Global Quote"]:
            raise ValueError(f"No data found for symbol: {symbol}")

        quote = data["Global Quote"]

        # Parse and return clean quote data
        return {
            "symbol": quote.get("01. symbol", symbol.upper()),
            "price": float(quote.get("05. price", 0)),
            "open_price": float(quote.get("02. open", 0)),
            "high_price": float(quote.get("03. high", 0)),
            "low_price": float(quote.get("04. low", 0)),
            "volume": int(quote.get("06. volume", 0)),
            "timestamp": datetime.utcnow(),
            "raw": quote,  # Keep raw data for debugging
        }

    async def get_intraday(
        self,
        symbol: str,
        interval: str = "60min",
    ) -> Dict[str, Any]:
        """
        Get intraday time series data

        Args:
            symbol: Stock symbol
            interval: Time interval (1min, 5min, 15min, 30min, 60min)

        Returns:
            Intraday data with timestamps and prices
        """
        endpoint = "/query"
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol.upper(),
            "interval": interval,
        }

        data = await self._make_request(endpoint, params)

        key = f"Time Series ({interval})"
        if key not in data:
            raise ValueError(f"No intraday data found for {symbol}")

        time_series = data[key]

        # Convert to list of price records
        prices = []
        for timestamp_str, price_data in time_series.items():
            prices.append({
                "timestamp": datetime.fromisoformat(timestamp_str),
                "open": float(price_data.get("1. open", 0)),
                "high": float(price_data.get("2. high", 0)),
                "low": float(price_data.get("3. low", 0)),
                "close": float(price_data.get("4. close", 0)),
                "volume": int(price_data.get("5. volume", 0)),
            })

        return {
            "symbol": symbol.upper(),
            "interval": interval,
            "prices": prices,
            "raw": data,
        }

    async def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get company information

        Args:
            symbol: Stock symbol

        Returns:
            Company information (name, sector, description)
        """
        endpoint = "/query"
        params = {
            "function": "OVERVIEW",
            "symbol": symbol.upper(),
        }

        data = await self._make_request(endpoint, params)

        if not data or "Symbol" not in data:
            raise ValueError(f"No company data found for {symbol}")

        return {
            "symbol": data.get("Symbol", symbol.upper()),
            "name": data.get("Name", ""),
            "sector": data.get("Sector", ""),
            "industry": data.get("Industry", ""),
            "market_cap": data.get("MarketCapitalization", ""),
            "pe_ratio": data.get("PERatio", ""),
            "description": data.get("Description", ""),
            "raw": data,
        }


async def fetch_stock_quote(symbol: str) -> Dict[str, Any]:
    """
    Convenience function to fetch stock quote

    Args:
        symbol: Stock symbol

    Returns:
        Quote data

    Example:
        >>> quote = await fetch_stock_quote("AAPL")
        >>> print(quote['price'])
    """
    async with AlphaVantageClient() as client:
        return await client.get_quote(symbol)


async def fetch_multiple_quotes(symbols: list[str]) -> Dict[str, Any]:
    """
    Fetch quotes for multiple stocks concurrently

    Args:
        symbols: List of stock symbols

    Returns:
        Dictionary with symbol -> quote mapping

    Example:
        >>> quotes = await fetch_multiple_quotes(["AAPL", "GOOGL", "MSFT"])
        >>> for symbol, quote in quotes.items():
        ...     print(f"{symbol}: ${quote['price']}")
    """
    async with AlphaVantageClient() as client:
        tasks = [client.get_quote(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        quotes = {}
        for symbol, result in zip(symbols, results):
            if isinstance(result, Exception):
                logger.error(f"Failed to fetch {symbol}: {result}")
                quotes[symbol] = None
            else:
                quotes[symbol] = result

        return quotes
