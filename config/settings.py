"""
Configuration management for the stock pipeline
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DB_DIR = BASE_DIR / "data"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./stock_data.db")

# API Configuration
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
API_BASE_URL = "https://www.alphavantage.co"
API_TIMEOUT = 10  # seconds

# Server
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))

# Processing
BATCH_SIZE = 5
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

class Config:
    """Configuration class for easy access"""
    db_url = DATABASE_URL
    api_key = ALPHA_VANTAGE_API_KEY
    api_base_url = API_BASE_URL
    api_timeout = API_TIMEOUT
    server_host = SERVER_HOST
    server_port = SERVER_PORT
    batch_size = BATCH_SIZE
    max_retries = MAX_RETRIES
