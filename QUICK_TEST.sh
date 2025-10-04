#!/bin/bash

echo "🧪 Testing Airflow Python Environment"
echo "======================================"

# Test 1: Check if containers are running
echo ""
echo "1️⃣  Checking Docker containers..."
if docker-compose ps | grep -q "airflow_scheduler.*Up"; then
    echo "   ✅ Airflow scheduler is running"
else
    echo "   ❌ Airflow scheduler is not running"
    echo "   Run: docker-compose up -d"
    exit 1
fi

# Test 2: Check file structure
echo ""
echo "2️⃣  Checking file structure..."
if [ -f "airflow/dags/utils/__init__.py" ]; then
    echo "   ✅ utils/__init__.py exists"
else
    echo "   ❌ utils/__init__.py missing"
    echo "   Run: touch airflow/dags/utils/__init__.py"
fi

if [ -f "airflow/dags/utils/api_clients.py" ]; then
    echo "   ✅ utils/api_clients.py exists"
else
    echo "   ❌ utils/api_clients.py missing"
fi

if [ -f "airflow/dags/utils/db_helpers.py" ]; then
    echo "   ✅ utils/db_helpers.py exists"
else
    echo "   ❌ utils/db_helpers.py missing"
fi

# Test 3: Test imports inside container
echo ""
echo "3️⃣  Testing imports in Airflow container..."
docker-compose exec -T airflow_scheduler python3 << 'PYTHON'
import sys
import os
sys.path.insert(0, '/opt/airflow/dags')
try:
    from utils.api_clients import get_fred_client
    from utils.db_helpers import get_db_hook
    print("   ✅ Imports successful!")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)
PYTHON

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 All tests passed! Your Airflow is Python-aware!"
    echo ""
    echo "Next steps:"
    echo "  1. Add your API keys to .env"
    echo "  2. Configure Airflow connection: timescaledb_conn"
    echo "  3. Trigger the economic_data_daily_update DAG"
else
    echo ""
    echo "⚠️  Some tests failed. Check the output above."
    echo ""
    echo "Quick fixes:"
    echo "  docker-compose restart airflow_scheduler"
    echo "  docker-compose exec airflow_scheduler touch /opt/airflow/dags/utils/__init__.py"
fi
