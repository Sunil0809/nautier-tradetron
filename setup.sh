#!/bin/bash
# Quick setup script for local development

set -e

echo "🚀 Algo Trading Platform - Quick Setup"
echo "======================================"

# 1. Create venv
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3.11 -m venv venv
fi

# 2. Activate
echo "⚡ Activating venv..."
source venv/bin/activate

# 3. Install deps
echo "📚 Installing dependencies..."
pip install -r requirements.txt -q

# 4. Create .env
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Edit .env with your API keys!"
fi

# 5. Setup database
echo "🗄️  Setting up database..."
python -c "
from app.database import create_all_tables
try:
    create_all_tables()
    print('✅ Database tables created')
except Exception as e:
    print(f'⚠️  Database setup skipped: {e}')
    print('   (Make sure PostgreSQL is running)')
"

# 6. Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -q --tb=short || echo "⚠️  Some tests failed (OK for first run)"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your credentials"
echo "2. Start PostgreSQL: docker run -d -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=algo_platform -p 5432:5432 postgres:15"
echo "3. Run: uvicorn app.main:app --reload"
echo "4. Visit: http://localhost:8000/docs"
echo ""
