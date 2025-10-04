# Making Airflow Python-Aware

This guide explains how to properly set up Python imports in Airflow so your DAGs can find and use custom modules.

## 🐍 The Problem

Airflow DAGs run in a specific environment, and by default, they may not find custom Python modules in subdirectories like `utils/`.

## ✅ Solutions Implemented

### 1. **Path Manipulation in DAG File** (Current Method)

We've added this to the top of `economic_data_daily_update.py`:

```python
import sys
import os

# Add current directory to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Now you can import from utils/
from utils.api_clients import get_fred_client
from utils.db_helpers import get_db_hook, log_update
```

**How it works**:
- `os.path.dirname(__file__)` gets the directory where the DAG file is located
- `os.path.abspath()` converts it to an absolute path
- `sys.path.insert(0, ...)` adds it to the beginning of Python's module search path
- Now Python can find `utils/` subdirectory

### 2. **Proper Module Structure**

We've created proper Python packages:

```
airflow/
└── dags/
    ├── __init__.py                    # Makes dags a package
    ├── economic_data_daily_update.py  # Main DAG
    └── utils/
        ├── __init__.py                # Makes utils a package
        ├── api_clients.py             # API client classes
        └── db_helpers.py              # Database helper functions
```

Each `__init__.py` file makes the directory a Python package, even if it's empty.

## 🔧 Alternative Methods

### Method A: Set PYTHONPATH in Docker

Add to `docker-compose.yml`:

```yaml
airflow_webserver:
  environment:
    - PYTHONPATH=/opt/airflow/dags:/opt/airflow/plugins
```

### Method B: Use Airflow's Plugin System

Move utilities to the plugins folder:

```
airflow/
├── dags/
│   └── economic_data_daily_update.py
└── plugins/
    └── economic_utils/
        ├── __init__.py
        ├── api_clients.py
        └── db_helpers.py
```

Then import as:
```python
from economic_utils.api_clients import get_fred_client
```

### Method C: Install as Package

Create `setup.py` in the utils directory:

```python
from setuptools import setup, find_packages

setup(
    name='economic-data-utils',
    version='1.0.0',
    packages=find_packages(),
)
```

Install in Airflow container:
```bash
pip install -e /opt/airflow/dags/utils
```

## 🧪 Testing Your Setup

### 1. Test Import in Airflow Container

```bash
# Access Airflow scheduler container
docker-compose exec airflow_scheduler bash

# Test Python imports
python3 << EOF
import sys
sys.path.insert(0, '/opt/airflow/dags')
from utils.api_clients import get_fred_client
print("Import successful!")
EOF
```

### 2. Test in Airflow UI

1. Go to Airflow UI: http://localhost:8080
2. Navigate to `economic_data_daily_update` DAG
3. Trigger the DAG manually
4. Check logs for any import errors

### 3. Check DAG Parsing

In Airflow UI, look for:
- DAG should appear without errors
- No red "Import Error" messages
- DAG should be parse-able

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'utils'`

**Solution 1**: Check `__init__.py` exists
```bash
docker-compose exec airflow_scheduler ls -la /opt/airflow/dags/utils/
```

Should show:
```
__init__.py
api_clients.py
db_helpers.py
```

**Solution 2**: Verify path insertion
Add debug prints to your DAG:
```python
import sys
import os

dag_dir = os.path.abspath(os.path.dirname(__file__))
print(f"DAG directory: {dag_dir}")
print(f"sys.path: {sys.path}")

sys.path.insert(0, dag_dir)
```

**Solution 3**: Use absolute imports
Instead of:
```python
from utils.api_clients import get_fred_client
```

Try:
```python
from dags.utils.api_clients import get_fred_client
```

### Issue: `ImportError: cannot import name 'get_fred_client'`

**Check the function exists**:
```bash
docker-compose exec airflow_scheduler grep "def get_fred_client" /opt/airflow/dags/utils/api_clients.py
```

**Verify syntax**:
```bash
docker-compose exec airflow_scheduler python3 -m py_compile /opt/airflow/dags/utils/api_clients.py
```

### Issue: Imports work locally but not in Airflow

**Possible causes**:
1. File permissions
2. Volume mounting issues
3. Different Python versions

**Solution**:
```bash
# Check file permissions
docker-compose exec airflow_scheduler ls -la /opt/airflow/dags/utils/

# Fix permissions if needed
docker-compose exec airflow_scheduler chmod -R 755 /opt/airflow/dags/utils/

# Restart Airflow
docker-compose restart airflow_scheduler airflow_webserver
```

## 📁 Recommended Project Structure

```
PortfolioManagementData/
└── airflow/
    ├── dags/
    │   ├── __init__.py                    # Empty or package init
    │   ├── economic_data_daily_update.py  # Main DAG
    │   ├── another_dag.py                 # Another DAG
    │   └── utils/                         # Shared utilities
    │       ├── __init__.py
    │       ├── api_clients.py
    │       ├── db_helpers.py
    │       └── data_validators.py
    │
    ├── plugins/                           # Custom operators/sensors
    │   └── custom_operators/
    │       ├── __init__.py
    │       └── economic_data_operator.py
    │
    └── logs/                              # Airflow logs
```

## 🔍 Verification Checklist

- [ ] `__init__.py` exists in `airflow/dags/`
- [ ] `__init__.py` exists in `airflow/dags/utils/`
- [ ] Path insertion code at top of DAG file
- [ ] Import statements use correct module names
- [ ] Files have proper permissions (644 or 755)
- [ ] DAG appears in Airflow UI without errors
- [ ] Test import in Airflow container works
- [ ] DAG can be triggered successfully

## 💡 Best Practices

### 1. Use Relative Imports Within Package

In `utils/db_helpers.py`:
```python
# Good: Relative import within package
from .api_clients import get_fred_client

# Also good: Absolute import with package name
from utils.api_clients import get_fred_client
```

### 2. Keep DAG Files Clean

Move complex logic to utils:
```python
# In DAG file - keep it simple
from utils.api_clients import get_fred_client
from utils.db_helpers import update_data

def update_task(**context):
    client = get_fred_client()
    data = client.get_series('GDP')
    update_data('macro', 'gdp', data)
```

### 3. Add Type Hints

```python
from typing import Optional, List
import pandas as pd

def get_series(series_id: str, start_date: Optional[str] = None) -> pd.DataFrame:
    """Get time series data"""
    pass
```

### 4. Document Your Modules

```python
"""
API Clients for Economic Data Sources

This module provides client classes for various economic data APIs:
- FREDClient: Federal Reserve Economic Data
- BLSClient: Bureau of Labor Statistics
- EIAClient: Energy Information Administration

Usage:
    from utils.api_clients import get_fred_client
    
    client = get_fred_client()
    data = client.get_series('GDP')
"""
```

## 🚀 Quick Fix Commands

If imports aren't working, run these:

```bash
# 1. Ensure __init__.py files exist
docker-compose exec airflow_scheduler touch /opt/airflow/dags/__init__.py
docker-compose exec airflow_scheduler touch /opt/airflow/dags/utils/__init__.py

# 2. Fix permissions
docker-compose exec airflow_scheduler chmod -R 755 /opt/airflow/dags

# 3. Restart Airflow services
docker-compose restart airflow_scheduler airflow_webserver airflow_worker

# 4. Clear Airflow cache
docker-compose exec airflow_scheduler airflow dags list

# 5. Test import
docker-compose exec airflow_scheduler python3 -c "
import sys
sys.path.insert(0, '/opt/airflow/dags')
from utils.api_clients import get_fred_client
print('Import successful!')
"
```

## 📚 Additional Resources

- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Python Packaging Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Python Import System](https://docs.python.org/3/reference/import.html)

---

**Summary**: Your Airflow environment is now Python-aware! The DAGs can import from the `utils/` directory thanks to proper path manipulation and package structure.
