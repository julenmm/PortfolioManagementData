"""
Superset configuration for Portfolio Management
"""

import os
from datetime import timedelta

# Superset specific configuration
ROW_LIMIT = 5000
SUPERSET_WEBSERVER_PORT = 8088

# Flask App Builder configuration
APP_NAME = "Portfolio Management Dashboard"
APP_ICON = "/static/assets/images/superset-logo@2x.png"
APP_THEME = "light"

# Database configuration - Using shared TimescaleDB
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SUPERSET_DATABASE_URL',
    f"postgresql://{os.environ.get('DATABASE_USER', 'portfolio_user')}:{os.environ.get('DATABASE_PASSWORD', 'portfolio_secure_password_2024')}@{os.environ.get('DATABASE_HOST', 'timescaledb')}:5432/{os.environ.get('DATABASE_DB', 'superset_db')}"
)

# Redis configuration - Using shared Redis
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = 1  # Use DB 1 for Superset (Django uses 0)

# Cache configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': REDIS_PORT,
    'CACHE_REDIS_DB': REDIS_DB,
}

# Data cache configuration
DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24,  # 1 day
    'CACHE_KEY_PREFIX': 'superset_data_',
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': REDIS_PORT,
    'CACHE_REDIS_DB': REDIS_DB,
}

# Results backend configuration
RESULTS_BACKEND = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24,  # 1 day
    'CACHE_KEY_PREFIX': 'superset_results_',
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': REDIS_PORT,
    'CACHE_REDIS_DB': REDIS_DB,
}

# Feature flags
FEATURE_FLAGS = {
    'ENABLE_TEMPLATE_PROCESSING': True,
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'DASHBOARD_RBAC': True,
    'ENABLE_ADVANCED_DATA_TYPES': True,
    'ENABLE_EXPLORE_JSON_CSRF_PROTECTION': False,
    'ENABLE_EXPLORE_DRAG_AND_DROP': True,
    'ENABLE_DASHBOARD_NATIVE_FILTERS': True,
    'ENABLE_FILTER_BOX_MIGRATION': True,
    'ENABLE_ADVANCED_DATA_TYPES': True,
    'GLOBAL_ASYNC_QUERIES': True,
    'ENABLE_TEMPLATE_PROCESSING': True,
    'ENABLE_EXPLORE_JSON_CSRF_PROTECTION': False,
    'ENABLE_EXPLORE_DRAG_AND_DROP': True,
    'ENABLE_DASHBOARD_NATIVE_FILTERS': True,
    'ENABLE_FILTER_BOX_MIGRATION': True,
    'ENABLE_ADVANCED_DATA_TYPES': True,
    'GLOBAL_ASYNC_QUERIES': True,
    'VERSIONED_EXPORT': True,
    'DASHBOARD_FILTERS_EXPERIMENTAL': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_NATIVE_FILTERS_SET': True,
    'DASHBOARD_FILTERS_EXPERIMENTAL': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_NATIVE_FILTERS_SET': True,
    'DASHBOARD_FILTERS_EXPERIMENTAL': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_NATIVE_FILTERS_SET': True,
}

# Security configuration
SECRET_KEY = os.environ.get('SUPERSET_SECRET_KEY', 'superset-secret-key-change-in-production-2024')

# JWT configuration for async queries (must be at least 32 bytes)
GLOBAL_ASYNC_QUERIES_JWT_SECRET = os.environ.get(
    'SUPERSET_JWT_SECRET_KEY',
    'superset-jwt-secret-key-for-async-queries-change-in-production-2024'
)

# CORS configuration
ENABLE_CORS = True
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['*']
}

# Authentication configuration
AUTH_TYPE = 1  # Database authentication
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = 'Public'

# Email configuration (optional)
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USERNAME = 'your-email@gmail.com'
# MAIL_PASSWORD = 'your-password'

# Logging configuration
LOG_LEVEL = 'INFO'

# Time zone configuration
DEFAULT_TIMEZONE = 'UTC'

# Custom CSS for branding
CUSTOM_CSS = """
/* Custom CSS for Portfolio Management Dashboard */
.navbar-brand {
    font-weight: bold;
    color: #1f77b4 !important;
}

.navbar-brand:hover {
    color: #ff7f0e !important;
}

/* Custom styling for charts */
.superset-chart-container {
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Dashboard title styling */
.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
}
"""

# Custom JavaScript for additional functionality
CUSTOM_JS = """
// Custom JavaScript for Portfolio Management Dashboard
console.log('Portfolio Management Dashboard loaded');

// Add custom functionality here
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard DOM loaded');
    
    // Add any custom JavaScript functionality
    // For example, custom chart interactions, data formatting, etc.
});
"""

# Database connection configurations
DATABASE_CONNECTIONS = {
    'timescaledb': {
        'display_name': 'TimescaleDB (Portfolio Data)',
        'description': 'Main database for portfolio management data',
        'sqlalchemy_uri': 'postgresql://portfolio_user:portfolio_secure_password_2024@timescaledb:5432/portfolio_management',
        'extra': {
            'engine_params': {
                'pool_size': 10,
                'max_overflow': 20,
                'pool_timeout': 30,
                'pool_recycle': 3600,
            }
        }
    }
}

# Custom SQL Lab configuration
SQL_LAB_DEFAULT_DBID = 1
SQLLAB_TIMEOUT = 300
SQLLAB_CTAS_NO_LIMIT = True

# Dashboard configuration
DASHBOARD_POSITION_DATA_LIMIT = 65535
DASHBOARD_NATIVE_FILTERS = True
DASHBOARD_CROSS_FILTERS = True

# Chart configuration
CHART_DEFAULT_CONFIG = {
    'colorScheme': 'supersetColors',
    'datasource': None,
    'sliceId': None,
    'urlParams': {},
    'formData': {},
    'queryContext': None,
    'hooks': {},
    'ownState': {},
    'filterState': {},
    'setDataMask': None,
    'setControlValue': None,
    'setTooltip': None,
}

# Export configuration
EXPORT_FORMATS = ['csv', 'xlsx', 'json']
EXPORT_FILENAME = 'superset_export'

# Performance configuration
SUPERSET_WEBSERVER_TIMEOUT = 60
SUPERSET_WEBSERVER_THREADS = 8
SUPERSET_WEBSERVER_WORKERS = 1

# Celery configuration for async tasks
class CeleryConfig:
    BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
    CELERY_IMPORTS = ('superset.sql_lab', 'superset.tasks')
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
    CELERY_TASK_PROTOCOL = 1

CELERY_CONFIG = CeleryConfig
