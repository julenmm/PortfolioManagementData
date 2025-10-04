#!/bin/bash

# =============================================================================
# DEVELOPMENT ENVIRONMENT STARTUP SCRIPT
# No Airflow Scheduler - Manual DAG triggering only
# =============================================================================

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   🚀 Starting Portfolio Management Stack - DEVELOPMENT        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "   Please create .env file with required environment variables"
    exit 1
fi

echo "📋 Development Mode Features:"
echo "   ✅ Django with hot-reload (runserver)"
echo "   ✅ Airflow Webserver (manual DAG triggering)"
echo "   ❌ Airflow Scheduler (DISABLED - no automatic runs)"
echo "   ✅ Superset with reload enabled"
echo ""
echo "🔧 Simplified Architecture:"
echo "   • 1 PostgreSQL (TimescaleDB) for all services"
echo "   • 1 Redis for all message brokers/caches"
echo "   • ~9 containers (down from 13-17!)"
echo ""

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start services
echo ""
echo "🏗️  Building services..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   ✅ DEVELOPMENT STACK STARTED SUCCESSFULLY!                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Access Services:"
echo "   • Django Backend:     http://localhost:8000"
echo "   • Airflow UI:         http://localhost:8080"
echo "   • PGAdmin:            http://localhost:5050"
echo "   • Superset:           http://localhost:8088"
echo ""
echo "🔑 Default Credentials:"
echo "   Airflow:  admin / airflow_secure_password_2024"
echo "   Superset: admin / superset_secure_password_2024"
echo "   PGAdmin:  admin@portfolio.com / pgadmin_secure_password_2024"
echo ""
echo "⚠️  DEVELOPMENT MODE:"
echo "   • Airflow Scheduler is DISABLED"
echo "   • DAGs must be triggered manually in the UI"
echo "   • Django uses runserver (for development only)"
echo "   • All services have hot-reload enabled"
echo ""
echo "💡 To run with scheduler (production mode):"
echo "   ./start-prod.sh"
echo ""
echo "📝 View logs:"
echo "   docker-compose logs -f [service_name]"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
