# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PMRdataanalysis is a Django-based data integration and analysis platform for managing marketing research, sales reports, and supplier data across multiple business lines and integrated companies. The system uses PostgreSQL with multiple database schemas and Redis for caching.

## Development Environment Setup

### Virtual Environment
```bash
# Activate virtual environment (Windows)
.PMRvenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Development Server
```bash
# Local development (default)
python manage.py runserver

# Production mode (requires changing manage.py line 12)
# Uncomment line 14 and comment line 12 in manage.py
```

### Database Management
```bash
# Run migrations
python manage.py migrate

# Create migrations for specific app
python manage.py makemigrations <app_name>

# Access Django shell
python manage.py shell
```

**IMPORTANT**: When modifying any `models.py` file (adding/changing fields, models, or choices), you MUST remind the user to run database migrations:
```bash
python manage.py makemigrations <app_name>
python manage.py migrate
```
However, note that many models in this project have `managed=False`, which means Django won't create/modify database tables. In these cases, database schema changes must be handled manually or through external migration tools.

### Static Files
```bash
# Collect static files (production)
python manage.py collectstatic
```

## Architecture

### Settings Configuration
- **Development**: `PMRdataanalysisV2/local_settings.py` (default in manage.py)
- **Production**: `PMRdataanalysisV2/production_settings.py` (CSRF disabled)
- Switch by modifying `DJANGO_SETTINGS_MODULE` in `manage.py` line 12/14

### Database Architecture
- **Database**: PostgreSQL with multiple schemas using search_path
- **Schemas**: django_admin_v2, marketing_research_v2, PMR_U8_001-012
- **Database Router**: `PMRdataanalysisV2/database_router.py` routes apps to specific databases
- **Connection**: Uses psycopg3 (`psycopg[binary]`)

Environment variables for database:
- `POSTGRESQL_INTERNAL_DBNAME`
- `POSTGRESQL_INTERNAL_USERNAME`
- `POSTGRESQL_INTERNAL_PASSWORD`
- `POSTGRESQL_INTERNAL_HOST`
- `POSTGRESQL_INTERNAL_PORT`

### Caching Layer
- **Backend**: Redis via django-redis
- **Database**: Redis DB #2
- Environment variables: `REDIS_INTERNAL_HOST`, `REDIS_INTERNAL_PORT`

### Application Structure

The project consists of multiple Django apps organized by business function:

**Direct Sales Research Apps:**
- `Mindray_Research` - Direct sales line A research
- `Marketing_Research` - Direct sales line B (legacy, mostly commented out)
- `Marketing_Research_QT` - QiTian direct sales
- `Marketing_Research_WD` - Direct sales line C
- `PMRKA` - KA customer research

**Agent/Distributor Apps:**
- `Marketing_Research_ZS` - Agent business research
- `Marketing_Research_Community` - Community hospital research

**Integrated Company Operations:**
- `PUZHONGXIN`, `XUERYUAN`, `ANTING`, `NANXIANG`, `XINYI`, `PIZHOU`, `SIWUWU` - Various integrated company battle plans

**Supply Chain Data Processing:**
- `SHIYUAN`, `GONGWEI`, `SHIYIBEI`, `SHIYINAN` - Supply chain data processing platforms
- `Suppliers` - Supplier information and ranking management

**ERP Integration:**
- `PMR_U8_001` through `PMR_U8_012` - U8 ERP synchronization for different business units

**Sales Reporting:**
- `SALESREPORT` - Integrated sales daily reports

### Data Processing Pattern

Several apps (`GONGWEI`, `SHIYUAN`, `SHIYIBEI`, `SHIYINAN`, `Suppliers`) follow a common pattern:
1. Excel file upload via web interface
2. Processing through `tools/CalculateAPI.py` functions
3. Pandas-based data transformation and aggregation
4. SQLAlchemy for bulk database operations
5. Multi-sheet Excel processing (orders, in/out inventory, consumption)

### Admin Interface Customization

- **Framework**: django-simpleui for enhanced admin UI
- **Custom Menu**: Extensively customized in `local_settings.py` SIMPLEUI_CONFIG
- **Language**: Chinese (zh-hans)
- **Timezone**: Asia/Shanghai
- **Custom User Model**: `Marketing_Research.UserInfo`
- **Session Duration**: 14 days

Key admin features:
- Custom filters in admin.py files (e.g., ProjectFilter, IfTargetCustomerFilter)
- Quarter-based target calculations via `Marketing_Research/tools/calculate_Quater_target.py`
- Nested admin for complex hierarchical data
- Date range filtering via django-admin-rangefilter

### URL Routing

Main URL patterns in `PMRdataanalysisV2/urls.py`:
- Root redirects to `/admin/`
- Each app has its own URL namespace
- AJAX endpoints for dynamic data (e.g., `/admin/get_models_by_brand/`)

## Deployment

### Docker Deployment
```bash
# Build Docker image
docker build -t pmrdataanalysis .

# Run with docker-compose
docker compose up -d
```

The Dockerfile:
- Base image: python:3.10
- Static files location: `/djangostatic`
- Working directory: `/pmrdataanalysis`
- Timezone: Asia/Shanghai

### CI/CD Pipeline
GitHub Actions workflow (`.github/workflows/deploy_to_ECS.yml`):
1. Triggers on push/PR to `main` branch
2. Builds Docker image with build args for secrets
3. Pushes to Alibaba Cloud Container Registry
4. SSH deploys to Alibaba Cloud ECS
5. Pulls new image and restarts services via docker-compose

## Important Implementation Notes

### Multi-Schema Database Pattern
When working with models:
- Models are distributed across different PostgreSQL schemas
- The database router (`database_router.py`) controls which app uses which database
- Always check `DATABASE_APPS_MAPPING` in settings when adding new apps

### Data Processing with Pandas
The `tools/CalculateAPI.py` modules use a consistent pattern:
- Read Excel sheets into pandas DataFrames
- Clean and transform data (astype conversions, groupby aggregations)
- Merge datasets from multiple sheets
- Write results back to PostgreSQL using SQLAlchemy engine

### Admin Customization
- Most business logic is in admin.py files using custom filters and methods
- Quarter-based calculations are centralized in `calculate_Quater_target.py`
- Menu configuration is entirely in settings, not code

### Static Files
Static files are distributed across apps:
- Each app has its own `static/<APP_NAME>/` directory
- Configured in `STATICFILES_DIRS` in settings
- Bootstrap, jQuery, and custom JS/CSS per app

### Security Notes
- Production settings disable CSRF (line 79 in production_settings.py)
- SECRET_KEY from environment variable in production
- Database credentials from environment variables
- Sensitive data passed as Docker build args in CI/CD
