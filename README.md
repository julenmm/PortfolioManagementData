# Portfolio Management Data Stack

A complete Docker-based stack for portfolio management and financial data analysis, featuring Django backend, Apache Airflow for data workflows, TimescaleDB for time-series data, and Apache Superset for data visualization.

## 🏗️ Architecture

- **Django Backend**: REST API for portfolio management
- **Apache Airflow**: Data workflow orchestration and ETL pipelines
- **TimescaleDB**: PostgreSQL with TimescaleDB extension for time-series data
- **Apache Superset**: Business intelligence and data visualization
- **PGAdmin4**: Database administration interface
- **Redis**: Caching and message broker

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd PortfolioManagementData
   ```

2. **Choose your mode:**

   **Development Mode** (No automatic scheduling, manual DAG triggers):
   ```bash
   ./start-dev.sh
   ```

   **Production Mode** (With automatic DAG scheduling):
   ```bash
   ./start-prod.sh
   ```

   Or manually:
   ```bash
   # Development
   docker-compose up --build -d
   
   # Production
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

   📖 **See [DOCKER_MODES.md](DOCKER_MODES.md) for detailed comparison**

### Service URLs

After startup, access the services at:

- **Django Backend**: http://localhost:8000
- **Apache Airflow**: http://localhost:8080
- **Apache Superset**: http://localhost:8088
- **PGAdmin4**: http://localhost:8080

### Default Credentials

- **Airflow**: admin / airflow_secure_password_2024
- **Superset**: admin / superset_secure_password_2024
- **PGAdmin**: admin@portfolio.com / pgadmin_secure_password_2024

## 📊 Database Schema

The TimescaleDB database includes:

- `portfolio.market_data`: Time-series market data
- `portfolio.portfolios`: Portfolio definitions
- `portfolio.holdings`: Current holdings
- `portfolio.transactions`: Transaction history
- `portfolio.performance`: Performance metrics

## 🔧 Configuration

All configuration is managed through the `.env` file. Key variables:

```env
# Database
POSTGRES_DB=portfolio_management
POSTGRES_USER=portfolio_user
POSTGRES_PASSWORD=portfolio_secure_password_2024

# Services
DJANGO_PORT=8000
AIRFLOW_PORT=8080
SUPERSET_PORT=8088
PGADMIN_PORT=8080
```

## 🛠️ Development

### Django Backend

```bash
# Access Django container
docker-compose exec django bash

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test
```

### Airflow DAGs

DAGs are located in `airflow/dags/`. The main pipeline:
- Extracts market data
- Transforms and cleans data
- Loads data to TimescaleDB
- Calculates portfolio metrics

### Superset Dashboards

- Access Superset at http://localhost:8088
- Connect to TimescaleDB using the provided connection string
- Create dashboards and charts for portfolio analysis

## 📈 Data Pipeline

The Airflow pipeline (`portfolio_data_pipeline`) runs daily and:

1. **Extract**: Fetches market data from financial APIs
2. **Transform**: Cleans and processes the data
3. **Load**: Stores data in TimescaleDB
4. **Analyze**: Calculates portfolio metrics and performance

## 🔍 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f django
docker-compose logs -f airflow_webserver
docker-compose logs -f superset_webserver
```

### Health Checks

```bash
# Check service status
docker-compose ps

# Check database connection
docker-compose exec timescaledb pg_isready -U portfolio_user -d portfolio_management
```

## 🗂️ Project Structure

```
PortfolioManagementData/
├── docker-compose.yml          # Main Docker Compose configuration
├── .env                        # Environment variables
├── start.sh                    # Startup script
├── backend/                    # Django backend
│   ├── Dockerfile
│   ├── requirements.txt
│   └── portfolio_management/
├── airflow/                    # Apache Airflow
│   ├── dags/
│   ├── logs/
│   └── plugins/
├── superset/                   # Apache Superset
│   └── superset_config.py
└── init-scripts/               # Database initialization
    └── init-timescaledb.sql
```

## 🔒 Security

**Important**: Change all default passwords in production:

1. Update passwords in `.env`
2. Generate new secret keys
3. Set `DEBUG_MODE=False`
4. Configure proper SSL certificates

## 🚨 Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 8000, 8080, 8088 are available
2. **Memory issues**: Increase Docker memory allocation
3. **Database connection**: Check TimescaleDB is running and accessible

### Reset Everything

```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Remove all images
docker-compose down --rmi all

# Start fresh
./start.sh
```

## 📚 API Documentation

Once running, access API documentation at:
- Django REST Framework: http://localhost:8000/api/
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the logs: `docker-compose logs -f [service]`
2. Review the troubleshooting section
3. Create an issue in the repository

---

**Happy Portfolio Management! 📊💰**
