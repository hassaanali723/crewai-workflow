# Stock Pipeline - Senior Python Engineer Interview Project

A **production-ready** real-time stock data ingestion pipeline demonstrating advanced Python concepts, async programming, database operations, and REST APIs.

## 🎯 Project Overview

This application demonstrates:
- ✅ **Async Programming**: Concurrent API calls with `asyncio` + `aiohttp`
- ✅ **Database Design**: ORM relationships with SQLAlchemy + async SQLite
- ✅ **Module Organization**: Clean architecture with separation of concerns
- ✅ **Data Validation**: Pydantic schemas for type safety
- ✅ **REST API**: FastAPI endpoints with proper error handling
- ✅ **Network Programming**: Retry logic, timeouts, error handling
- ✅ **Professional Practices**: Logging, configuration management, context managers

## 🛠 Technology Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| **Async** | `asyncio`, `aiohttp` | Concurrent API calls without blocking |
| **Database** | `SQLAlchemy` ORM + `aiosqlite` | Type-safe, async-friendly database operations |
| **REST API** | `FastAPI` + `Uvicorn` | Modern, high-performance API framework |
| **Validation** | `Pydantic` | Schema validation and type hints |
| **Configuration** | `python-dotenv` | Environment-based settings |
| **Logging** | Built-in `logging` | Structured logging for debugging |

## 📁 Project Structure

```
stock_pipeline/
├── src/
│   ├── api_clients/           # Alpha Vantage API client
│   │   ├── alphavantage.py   # Async HTTP client with retry logic
│   │   └── __init__.py
│   │
│   ├── database/              # Database layer
│   │   ├── connection.py      # Async SQLAlchemy setup
│   │   ├── models.py          # ORM models (Stock, StockPrice)
│   │   ├── crud.py            # CRUD operations (12 functions)
│   │   └── __init__.py
│   │
│   ├── models/                # Data schemas
│   │   ├── schemas.py         # Pydantic validation models
│   │   └── __init__.py
│   │
│   ├── processors/            # Data processing
│   │   ├── data_processor.py  # Validation and transformation
│   │   └── __init__.py
│   │
│   ├── server/                # REST API
│   │   ├── app.py            # FastAPI application (15 endpoints)
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── config/
│   └── settings.py            # Configuration management
│
├── main.py                    # Entry point (complete demo)
├── pyproject.toml             # Project metadata and dependencies
├── .env                       # Environment variables
└── README.md
```

## 📦 Installation

```bash
# Navigate to project directory
cd stock_pipeline

# Install dependencies
pip install -e .

# Install dev dependencies (optional)
pip install -e ".[dev]"
```

## 🚀 Running the Application

### Option 1: Run the Complete Pipeline

```bash
python main.py
```

This will:
1. Initialize the database
2. Fetch real stock data from Alpha Vantage API
3. Process and validate the data
4. Store in SQLite database
5. Display API endpoint information

### Option 2: Start the REST API Server

```bash
# Terminal 1: Start the API server
uvicorn src.server.app:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Make requests
curl http://localhost:8000/health
curl http://localhost:8000/stocks
curl http://localhost:8000/fetch/quote/AAPL
```

## 📚 API Endpoints

### Stock Management
```
POST   /stocks                          - Create a new stock
GET    /stocks                          - List all stocks (paginated)
GET    /stocks/{stock_id}               - Get stock with all prices
PUT    /stocks/{stock_id}               - Update stock info
DELETE /stocks/{stock_id}               - Delete stock
```

### Price Queries
```
GET    /stocks/symbol/{symbol}/latest   - Get latest price
GET    /stocks/symbol/{symbol}/prices   - Get all prices (paginated)
GET    /stocks/symbol/{symbol}/stats    - Get statistics (high/low/avg)
```

### External API Integration
```
POST   /fetch/quote/{symbol}                        - Fetch single stock from API
POST   /fetch/quotes?symbols=AAPL&symbols=GOOGL    - Fetch multiple stocks
```

### Utilities
```
GET    /health                          - Health check
GET    /docs                            - Interactive API documentation
GET    /redoc                           - ReDoc documentation
```

## 🧪 Example Usage

### 1. Fetch and Save Stock Data
```bash
# Fetch AAPL from Alpha Vantage API and save to database
curl -X POST http://localhost:8000/fetch/quote/AAPL

# Response:
{
  "id": 1,
  "stock_id": 1,
  "price": 150.50,
  "open_price": 149.00,
  "high_price": 151.00,
  "low_price": 148.50,
  "volume": 5000000,
  "timestamp": "2026-04-13T10:30:00",
  "created_at": "2026-04-13T10:30:00"
}
```

### 2. Get Latest Price
```bash
curl http://localhost:8000/stocks/symbol/AAPL/latest
```

### 3. Get Statistics
```bash
curl "http://localhost:8000/stocks/symbol/AAPL/stats?days=30"

# Response:
{
  "symbol": "AAPL",
  "period_days": 30,
  "high": 155.00,
  "low": 148.50,
  "avg": 150.75,
  "count": 30
}
```

## 💡 Interview Topics Covered

### 1. **Python Fundamentals**
- ✅ OOP design patterns
- ✅ Type hints and annotations
- ✅ Context managers (`async with`)
- ✅ Decorators and generators
- ✅ Exception handling

### 2. **Async Programming**
- ✅ `asyncio` event loop
- ✅ `async/await` syntax
- ✅ Concurrent execution with `gather()`
- ✅ Timeout handling
- ✅ Task management

### 3. **Database Design**
- ✅ ORM (SQLAlchemy) relationships
- ✅ One-to-Many relationships
- ✅ Async database operations
- ✅ CRUD operations
- ✅ Transactions and rollback

### 4. **API Design**
- ✅ RESTful principles
- ✅ HTTP methods (GET, POST, PUT, DELETE)
- ✅ Status codes (200, 404, 409, 500)
- ✅ Request/response schemas
- ✅ Error handling

### 5. **Architecture Patterns**
- ✅ Layered architecture
- ✅ Separation of concerns
- ✅ Dependency injection
- ✅ Error handling strategies

### 6. **Software Engineering Practices**
- ✅ Configuration management
- ✅ Logging and debugging
- ✅ Code organization and modularity
- ✅ Documentation (docstrings)
- ✅ Type safety with Pydantic

## 🔧 Configuration

Edit `.env` file to customize:
```env
# API Configuration
ALPHA_VANTAGE_API_KEY=demo
DATABASE_URL=sqlite+aiosqlite:///./stock_data.db

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Logging
LOG_LEVEL=INFO
```

## 📊 Data Flow

```
External API (Alpha Vantage)
    ↓
API Client (aiohttp - async)
    ↓
Data Processor (validate, transform)
    ↓
CRUD Functions (database operations)
    ↓
SQLAlchemy ORM Models
    ↓
SQLite Database
    ↓
REST API (FastAPI)
    ↓
Client (JSON response)
```

## 🎓 Key Design Decisions

| Decision | Reason |
|----------|--------|
| **Async/Await** | Fetch multiple API calls concurrently without blocking |
| **SQLAlchemy ORM** | Type-safe database operations, automatic relationship handling |
| **Pydantic Schemas** | Validate data early, catch errors immediately |
| **FastAPI** | Modern, performant, automatic API documentation |
| **Layered Architecture** | Separation of concerns, easy to test and maintain |
| **Context Managers** | Automatic resource cleanup (database connections) |

## ✨ What You'll Learn

This project is a complete example of production Python code:
- How to structure a Python project professionally
- Async programming patterns and best practices
- Database design and ORM usage
- REST API design with FastAPI
- Error handling and validation
- Configuration management
- Code organization and modularity

## 🚦 Getting Started for Interview

1. **Understand the flow**: `main.py` → API Client → Processor → Database → REST API
2. **Explore the code**: Start with `src/database/models.py` to understand data structures
3. **Try the API**: Run `main.py` to populate data, then test endpoints with curl
4. **Ask questions**: Understand WHY each technology choice was made
5. **Modify it**: Try adding a new endpoint or feature to show understanding

## 📝 Interview Questions You Should Be Able to Answer

- "Why use async/await instead of threading?"
- "What does ORM provide compared to raw SQL?"
- "How does Pydantic validation work?"
- "Why separate API client, processor, and CRUD layers?"
- "How does the database session lifecycle work?"
- "What's the difference between `flush()` and `commit()`?"
- "Why use context managers for database operations?"
- "How does the retry logic prevent rate limiting?"

## 🎯 Next Steps for Learning

1. Add unit tests with pytest
2. Implement caching with Redis
3. Add pagination for large datasets
4. Implement authentication with JWT
5. Add database migrations with Alembic
6. Deploy with Docker and Kubernetes
7. Add monitoring and metrics

---

**Good luck with your interview! 🚀**
