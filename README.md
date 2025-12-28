"""Project README and Getting Started Guide"""
# Algo Trading Platform

A production-grade, multi-user SaaS platform for algorithmic trading with:

- **Tradetron-style rule builder** (no-code)
- **Nautilus event-driven engine** (architecture)
- **Paper + Live trading** (complete separation)
- **FYERS integration** (Indian markets)
- **Risk management** (kill switch, daily loss limits)
- **SaaS monetization** (subscription plans)
- **India-compliant** (SEBI, audit logs)

## Quick Start

### 1. Environment Setup

```bash
python --version  # Should be 3.11+
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# PostgreSQL (required for production)
# For local dev, you can use SQLite:

# Create .env file
cp .env.example .env

# Edit .env with your database URL
```

### 3. Run Application

```bash
uvicorn app.main:app --reload
# API at: http://localhost:8000
# Docs at: http://localhost:8000/docs
```

## Project Structure

```
app/
├── api/           # REST endpoints (users, strategies, orders)
├── engine/        # Event queue & engine loop
├── events/        # Event definitions (market, signal, order, fill)
├── execution/     # Paper vs Live order execution
├── broker/        # FYERS API adapter
├── risk/          # Risk validation engine
├── models/        # Database models (users, strategies, orders)
├── database/      # DB connection & migrations
├── utils/         # Logging, alerts, config
└── main.py        # FastAPI app entry point
```

## Core Architecture

### Event Flow (Same for Paper & Live)

```
Market Data
    ↓
[Event Queue]
    ↓
Strategy (reads data, emits signals)
    ↓
Signal Event
    ↓
Risk Engine (validates)
    ↓
Order Event
    ↓
Execution Handler
    ├── Paper: Simulate (slippage, delays)
    └── Live: FYERS broker
    ↓
Fill Event
    ↓
Portfolio Update
```

## Key Files to Understand

| File | Purpose |
|------|---------|
| `events/__init__.py` | Event definitions (core) |
| `engine/__init__.py` | Event queue |
| `risk/__init__.py` | Risk validation |
| `execution/__init__.py` | Paper & Live handlers |
| `broker/__init__.py` | FYERS API wrapper |
| `models/__init__.py` | Database schema |
| `main.py` | FastAPI app |

## Phase Checklist

- [x] Phase 1: Create Codespace project
- [x] Phase 2: Project structure
- [x] Phase 3: Event-driven engine
- [ ] Phase 4: Rule engine (JSON rules parser)
- [ ] Phase 5: Risk engine (implemented, needs testing)
- [ ] Phase 6: Order state machine
- [ ] Phase 7: Paper vs Live (implemented, needs testing)
- [ ] Phase 8: Realistic paper trading
- [ ] Phase 9: FYERS live execution
- [ ] Phase 10: Multi-user & database
- [ ] Phase 11: Subscription & pricing
- [ ] Phase 12: India/SEBI compliance
- [ ] Phase 13: Monitoring & alerts
- [ ] Phase 14: CI/CD & deployment
- [ ] Phase 15: Final verification

## Next Steps

1. **Add authentication API** (JWT)
2. **Create strategy builder API** (JSON rule validation)
3. **Add websocket for live market data**
4. **Implement Telegram alerts**
5. **Add PostgreSQL setup script**
6. **Write integration tests**

## Important Rules

⚠️ **Never forget these:**

- Strategy ≠ Order placement (always go through signals)
- Every order has client_order_id (idempotency)
- Risk checks ALL signals before orders
- Paper trading ≠ Live (use different tables)
- Kill switch always visible
- Log everything (audit trail)
- User_id scopes everything

## Database

For production, use PostgreSQL:

```bash
# Create database
createdb algo_platform

# Run migrations
alembic upgrade head
```

For local testing, edit `.env`:
```
DATABASE_URL=sqlite:///algo_platform.db
```

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=app
```

## Deployment

See `DEPLOYMENT.md` for Docker, GitHub Actions, and VPS setup.

---

**Status**: Phase 2 Complete ✅  
**Next**: Phase 4 (Rule Engine)
