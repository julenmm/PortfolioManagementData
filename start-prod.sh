#!/bin/bash

# =============================================================================
# PRODUCTION ENVIRONMENT STARTUP SCRIPT
# With Airflow Scheduler - Automated DAG scheduling
# =============================================================================

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   🚀 Starting Portfolio Management Stack - PRODUCTION         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "   Please create .env file with required environment variables"
    exit 1
fi

# Check if API keys are set
echo "🔍 Checking API keys..."
if grep -q "your_actual_key_here" .env || grep -q "CHANGE_THIS" .env; then
    echo "⚠️  WARNING: Some API keys appear to be placeholder values"
    echo "   Please update .env with actual API keys before running in production"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "📋 Production Mode Features:"
echo "   ✅ Django with Gunicorn (production server)"
echo "   ✅ Airflow Webserver"
echo "   ✅ Airflow Scheduler (ENABLED - automatic DAG runs)"
echo "   ✅ Airflow Worker (Celery executor)"
echo "   ✅ Airflow Flower (Celery monitoring)"
echo "   ✅ Superset with Gunicorn"
echo "   ✅ All services with restart=always"
echo ""

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

# Build and start services
echo ""
echo "🏗️  Building services..."
docker-compose -f docker-compose.prod.yml build

echo ""
echo "🚀 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to start..."
echo "   (This may take 1-2 minutes for first-time initialization)"
sleep 30

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   ✅ PRODUCTION STACK STARTED SUCCESSFULLY!                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Access Services:"
echo "   • Django Backend:     http://localhost:8000"
echo "   • Airflow UI:         http://localhost:8080"
echo "   • Airflow Flower:     http://localhost:5555"
echo "   • PGAdmin:            http://localhost:8080"
echo "   • Superset:           http://localhost:8088"
echo ""
echo "🔑 Default Credentials:"
echo "   Airflow:  admin / airflow_secure_password_2024"
echo "   Superset: admin / superset_secure_password_2024"
echo "   PGAdmin:  admin@portfolio.com / pgadmin_secure_password_2024"
echo ""
echo "🔄 PRODUCTION MODE - Scheduler Active:"
echo "   • DAGs will run automatically on schedule"
echo "   • economic_data_daily_update: Daily at 6 AM"
echo "   • Monitor progress in Airflow UI"
echo "   • View Celery workers in Flower UI"
echo ""
echo "⚡ Next Steps:"
echo "   1. Configure Airflow connection: timescaledb_conn"
echo "      Admin → Connections → Add Connection"
echo "   2. Unpause DAGs in Airflow UI"
echo "   3. Monitor first run in Airflow logs"
echo "   4. Connect Superset to TimescaleDB"
echo ""
echo "📝 View logs:"
echo "   docker-compose -f docker-compose.prod.yml logs -f [service_name]"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose -f docker-compose.prod.yml down"
echo ""
echo "⚠️  SECURITY REMINDERS:"
echo "   • Change all default passwords in .env"
echo "   • Update Django SECRET_KEY and ALLOWED_HOSTS"
echo "   • Enable SSL/TLS in production"
echo "   • Set up firewall rules"
echo "   • Configure backup procedures"
echo ""
