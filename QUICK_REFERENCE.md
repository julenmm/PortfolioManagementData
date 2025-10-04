# 🚀 Quick Reference Card

## Start Commands

```bash
# Development (no scheduler)
./start-dev.sh

# Production (with scheduler)
./start-prod.sh
```

## Stop Commands

```bash
# Development
docker-compose down

# Production
docker-compose -f docker-compose.prod.yml down
```

## View Logs

```bash
# Development
docker-compose logs -f [service_name]

# Production
docker-compose -f docker-compose.prod.yml logs -f [service_name]

# Examples
docker-compose logs -f airflow_webserver
docker-compose -f docker-compose.prod.yml logs -f airflow_scheduler
```

## Service URLs

| Service | URL | Dev | Prod |
|---------|-----|-----|------|
| Django | http://localhost:8000 | ✅ | ✅ |
| Airflow UI | http://localhost:8080 | ✅ | ✅ |
| Airflow Flower | http://localhost:5555 | ❌ | ✅ |
| PGAdmin | http://localhost:8080 | ✅ | ✅ |
| Superset | http://localhost:8088 | ✅ | ✅ |

## Default Credentials

```
Airflow:  admin / airflow_secure_password_2024
Superset: admin / superset_secure_password_2024
PGAdmin:  admin@portfolio.com / pgadmin_secure_password_2024
```

## Key Differences

| Feature | Development | Production |
|---------|-------------|------------|
| Airflow Scheduler | ❌ Disabled | ✅ Enabled |
| DAG Execution | Manual only | Automatic |
| Django Server | runserver | gunicorn |
| Hot Reload | ✅ Yes | ❌ No |

## Common Tasks

### Trigger DAG Manually (Dev Mode)
1. Go to Airflow UI: http://localhost:8080
2. Find DAG: `economic_data_daily_update`
3. Click Play button ▶️

### Check Service Status
```bash
docker-compose ps
docker-compose -f docker-compose.prod.yml ps
```

### Restart Service
```bash
docker-compose restart django
docker-compose -f docker-compose.prod.yml restart airflow_scheduler
```

### Access Database
```bash
docker-compose exec timescaledb psql -U portfolio_user -d portfolio_management
```

### Configure Airflow Connection
1. Airflow UI → Admin → Connections
2. Add connection:
   - Conn Id: `timescaledb_conn`
   - Type: `Postgres`
   - Host: `timescaledb`
   - Schema: `portfolio_management`
   - Login: `portfolio_user`
   - Password: `portfolio_secure_password_2024`
   - Port: `5432`

## Files & Documentation

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Development mode |
| `docker-compose.prod.yml` | Production mode |
| `start-dev.sh` | Start dev mode |
| `start-prod.sh` | Start prod mode |
| `.env` | Configuration |
| `DOCKER_MODES.md` | Detailed comparison |
| `API_KEYS_SETUP.md` | API key setup guide |
| `AIRFLOW_PYTHON_SETUP.md` | Python import guide |

## Troubleshooting

**DAGs not running?**
- In dev mode: This is normal, trigger manually
- In prod mode: Check scheduler logs

**Import errors?**
- See `AIRFLOW_PYTHON_SETUP.md`
- Run `./QUICK_TEST.sh`

**Services won't start?**
```bash
docker-compose down -v
docker-compose up --build -d
```

**Need help?**
- Check logs: `docker-compose logs -f [service]`
- Review `DOCKER_MODES.md`
- Check `README.md`
