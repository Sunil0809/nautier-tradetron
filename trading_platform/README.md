# Trading Platform (Tradetron-like)

Production-ready modular algorithmic trading platform with Django + DRF + Channels backend, React + TypeScript + Tailwind frontend, Celery workers, PostgreSQL/Redis infrastructure, backtesting and execution engine.

## Structure

- `backend/` Django project and domain apps (`users`, `strategies`, `execution`, `backtesting`, `marketplace`, `copytrading`, `risk`, `portfolio`, `monitoring`, `datafeed`).
- `frontend/` React SPA pages for dashboard, strategy builder, backtests, marketplace, portfolio.
- `workers/` Specialized worker entrypoints.
- `infrastructure/` Docker Compose for cloud/deployment bootstrap.

## Run (Docker)

```bash
cd trading_platform
cp .env.example .env
cd infrastructure
docker compose up --build
```

## Run backend locally

```bash
cd trading_platform/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
USE_SQLITE=1 python manage.py migrate
USE_SQLITE=1 python manage.py runserver
```

## Run tests

```bash
cd trading_platform/backend
USE_SQLITE=1 pytest
```
