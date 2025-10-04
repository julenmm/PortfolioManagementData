# 🐳 Docker Compose Modes - Development vs Production

## Overview

This project provides two separate Docker Compose configurations:

| Mode | File | Airflow Scheduler | Use Case |
|------|------|-------------------|----------|
| **Development** | `docker-compose.yml` | ❌ Disabled | Local development, testing DAGs manually |
| **Production** | `docker-compose.prod.yml` | ✅ Enabled | Production deployment, automated scheduling |

---

## 🛠️ Development Mode

### File: `docker-compose.yml`

**When to Use:**
- Local development
- Testing and debugging DAGs
- Rapid iteration on code
- Manual DAG execution only

### Key Features:
- ✅ Django with `runserver` (hot-reload)
- ✅ Airflow Webserver (manual triggering)
- ❌ **No Airflow Scheduler** (DAGs don't run automatically)
- ✅ Superset with reload enabled
- ✅ `restart: unless-stopped`
- ✅ `DEBUG=True` for Django

### Services Included:
```
✅ timescaledb        - Database
✅ pgadmin            - DB Management
✅ redis              - Message broker
✅ django             - Backend (dev server)
✅ celery_worker      - Task worker
✅ celery_beat        - Scheduled tasks
✅ airflow_postgres   - Airflow DB
✅ airflow_redis      - Airflow broker
✅ airflow_webserver  - Airflow UI ONLY
✅ superset_*         - Analytics platform

❌ airflow_scheduler  - DISABLED
❌ airflow_worker     - DISABLED  
❌ airflow_flower     - DISABLED
```

### Start Development Mode:

```bash
# Quick start
./start-dev.sh

# Or manually
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Access Services:
- **Django**: http://localhost:8000
- **Airflow UI**: http://localhost:8080
- **PGAdmin**: http://localhost:8080
- **Superset**: http://localhost:8088

### Triggering DAGs in Dev Mode:

Since the scheduler is disabled, you must trigger DAGs manually:

1. Go to Airflow UI: http://localhost:8080
2. Find your DAG (e.g., `economic_data_daily_update`)
3. Click the **Play button** ▶️ to trigger manually
4. Monitor execution in Graph View

---

## 🚀 Production Mode

### File: `docker-compose.prod.yml`

**When to Use:**
- Production deployment
- Automated data pipelines
- Scheduled DAG execution
- 24/7 operation

### Key Features:
- ✅ Django with `gunicorn` (production server)
- ✅ Airflow Webserver
- ✅ **Airflow Scheduler** (DAGs run automatically)
- ✅ Airflow Worker (Celery executor)
- ✅ Airflow Flower (Celery monitoring)
- ✅ Superset with Gunicorn
- ✅ `restart: always` (auto-restart on failure)
- ✅ `DEBUG=False` for Django
- ✅ Production-ready configurations

### Services Included:
```
✅ timescaledb        - Database
✅ pgadmin            - DB Management
✅ redis              - Message broker
✅ django             - Backend (Gunicorn)
✅ celery_worker      - Task worker
✅ celery_beat        - Scheduled tasks
✅ airflow_postgres   - Airflow DB
✅ airflow_redis      - Airflow broker
✅ airflow_webserver  - Airflow UI
✅ airflow_scheduler  - ENABLED (automatic runs)
✅ airflow_worker     - ENABLED (task execution)
✅ airflow_flower     - ENABLED (monitoring)
✅ superset_*         - Analytics platform
```

### Start Production Mode:

```bash
# Quick start
./start-prod.sh

# Or manually
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop
docker-compose -f docker-compose.prod.yml down
```

### Access Services:
- **Django**: http://localhost:8000
- **Airflow UI**: http://localhost:8080
- **Airflow Flower**: http://localhost:5555 (NEW!)
- **PGAdmin**: http://localhost:8080
- **Superset**: http://localhost:8088

### Scheduler Behavior:

DAGs run automatically on their schedule:
- `economic_data_daily_update`: Daily at 6 AM
- Monitor progress in Airflow UI → DAGs → Graph View
- View worker status in Flower UI

---

## 📊 Comparison Table

| Feature | Development | Production |
|---------|-------------|------------|
| **Airflow Scheduler** | ❌ Disabled | ✅ Enabled |
| **Airflow Worker** | ❌ Disabled | ✅ Enabled |
| **Airflow Flower** | ❌ Disabled | ✅ Enabled |
| **Django Server** | runserver | gunicorn |
| **Superset Server** | dev mode | gunicorn |
| **Hot Reload** | ✅ Yes | ❌ No |
| **Debug Mode** | ✅ Yes | ❌ No |
| **Auto Restart** | unless-stopped | always |
| **DAG Execution** | Manual only | Automatic + Manual |
| **Celery Workers** | Basic | 4 workers |
| **Redis Persistence** | No appendonly | appendonly yes |

---

## 🔄 Switching Between Modes

### From Dev to Prod:

```bash
# Stop dev
docker-compose down

# Start prod
./start-prod.sh
```

### From Prod to Dev:

```bash
# Stop prod
docker-compose -f docker-compose.prod.yml down

# Start dev
./start-dev.sh
```

### Keep Both Running (Different Ports):

⚠️ **Not recommended** - Both use the same ports by default. You would need to:
1. Create a third compose file with different ports
2. Use different network names
3. Use different volume names

---

## 🎯 Typical Workflow

### 1. **Development Phase**

```bash
# Start dev mode
./start-dev.sh

# Develop and test your DAGs
# Trigger manually in Airflow UI

# Make changes to code
# Changes auto-reload (hot-reload)

# Test again
# Iterate...
```

### 2. **Testing Phase**

```bash
# Test with scheduler temporarily
docker-compose -f docker-compose.prod.yml up airflow_scheduler

# Verify schedule works
# Check logs

# Stop scheduler
docker-compose -f docker-compose.prod.yml stop airflow_scheduler
```

### 3. **Production Deployment**

```bash
# Update .env with production values
nano .env

# Start production stack
./start-prod.sh

# Monitor first run
docker-compose -f docker-compose.prod.yml logs -f airflow_scheduler

# Check Flower for worker status
open http://localhost:5555
```

---

## 🐛 Troubleshooting

### Issue: "DAGs not running in dev mode"

**Cause:** This is expected! Scheduler is disabled in dev mode.

**Solution:** Trigger manually or switch to prod mode.

### Issue: "DAGs running when I don't want them to"

**Cause:** You're in production mode with scheduler enabled.

**Solution:** Switch to dev mode:
```bash
docker-compose -f docker-compose.prod.yml down
./start-dev.sh
```

### Issue: "Can't access Flower UI"

**Cause:** Flower only runs in production mode.

**Solution:** Use production compose file:
```bash
./start-prod.sh
```

### Issue: "Service won't start in prod mode"

**Cause:** Service might already be running in dev mode.

**Solution:**
```bash
# Stop all containers
docker-compose down
docker-compose -f docker-compose.prod.yml down

# Start fresh
./start-prod.sh
```

---

## 📝 Configuration Tips

### Development Settings

In `.env`, ensure:
```env
DJANGO_DEBUG=True
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=true
```

### Production Settings

In `.env`, ensure:
```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,localhost
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=false

# Change all default passwords!
POSTGRES_PASSWORD=strong_password_here
DJANGO_SECRET_KEY=strong_secret_here
AIRFLOW_PASSWORD=strong_password_here
```

---

## 🔒 Security Checklist (Production)

Before deploying to production:

- [ ] Change all default passwords in `.env`
- [ ] Update `DJANGO_SECRET_KEY` to a strong random value
- [ ] Set `DJANGO_ALLOWED_HOSTS` to your domain
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Update `AIRFLOW_FERNET_KEY` (generate with `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`)
- [ ] Configure SSL/TLS certificates
- [ ] Set up firewall rules (restrict port access)
- [ ] Enable database backups
- [ ] Configure monitoring and alerts
- [ ] Review Airflow security settings
- [ ] Disable PGAdmin in production (or secure it properly)

---

## 📚 Quick Command Reference

### Development Mode
```bash
# Start
./start-dev.sh
docker-compose up -d

# Logs
docker-compose logs -f
docker-compose logs -f airflow_webserver

# Stop
docker-compose down

# Rebuild
docker-compose build
docker-compose up -d --build
```

### Production Mode
```bash
# Start
./start-prod.sh
docker-compose -f docker-compose.prod.yml up -d

# Logs
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml logs -f airflow_scheduler

# Stop
docker-compose -f docker-compose.prod.yml down

# Rebuild
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d --build
```

### Both Modes
```bash
# Check status
docker-compose ps
docker-compose -f docker-compose.prod.yml ps

# Restart a service
docker-compose restart django
docker-compose -f docker-compose.prod.yml restart airflow_scheduler

# Access container shell
docker-compose exec django bash
docker-compose exec timescaledb psql -U portfolio_user -d portfolio_management

# Remove volumes (CAUTION: deletes data!)
docker-compose down -v
docker-compose -f docker-compose.prod.yml down -v
```

---

## 🎓 Summary

**Choose Development Mode when:**
- You're actively developing and testing
- You want to trigger DAGs manually
- You need hot-reload for rapid iteration
- You're debugging issues

**Choose Production Mode when:**
- You want DAGs to run automatically on schedule
- You're deploying to production
- You need maximum reliability (restart=always)
- You want to monitor workers with Flower

**Remember:** Development mode = Manual control, Production mode = Automated scheduling! 🚀
