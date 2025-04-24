# CYSL Web Backend

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=CoastalYouthSoccer_cysl-backend&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=CoastalYouthSoccer_cysl-backend)

## Database Migrations

### Alembic Init

So I remember how to setup async database and `alembic` directory

`alembic init -t async alembic`

Update `alembic/script.py.mako` section
```
from alembic import op
import sqlalchemy as sa
import sqlmodel         #NEW
```

Update `alembic/env.py`:
```
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel                       # NEW

from alembic import context

from app.models import Season, Misconduct      # noqa
```

Replace line `target_metadata = None` with `target_metadata = SQLModel.metadata` 


### Generating Migrations

```
alembic revision --autogenerate -m "comment"
```

### Applying Migrations

```
alembic upgrade head
```

## Environment Variables

The system searches for environment variables in `.env` unless overridden by the environment variable, `ENV_FILE`.

### Required Environment Variables

`ASSIGNR_CLIENT_ID` - Assignr Client ID associated with your API environment.
`ASSIGNR_CLIENT_SECRET` - Assignr Client ID associated with your API environment.
`AUTH0_DOMAIN` - Domain name associated with the application.
`AUTH0_API_AUDIENCE` - Auth0 API Audience associated with this application.
`AUTH0_ISSUER` - Auth0 Issuer linked to this application.
`DATABASE_URL` - database connection string. MySQL and Postgres are currently supported.
   Postgres example: `postgresql+asyncpg://user:pass@localhost/dbname`
   MySql example: `mysql+asyncmy://user:pass@localhost/dbname`

### Optional Environment Variables

`ASSIGNR_AUTH_URL`- Assignr authorization url endpoint, defaults to `https://app.assignr.com/oauth/token`
`ASSIGNR_BASE_URL` - Base Assignr API endpoint, defaults to `https://api.assignr.com/api/v2/`
`ASSIGNR_CLIENT_SCOPE` - Assignr requested access, defaults to "read write"
`AUTH0_ALGORITHMS` - defaults to "RS256"
`HTTP_ORIGINS` - defaults to "*". Really should be changed to proper domain.
`LOG_LEVEL` - sets logging level. Needs to be integer value. Defaults to `30` (WARNING). Valid values:
  `0`  - NOTSET
  `10` - DEBUG
  `20` - INFO
  `30` - WARNING
  `40` - ERROR
  `50` - CRITICAL
 
 ## Running Unit Test Suite

 ### Creating the Test Database and User

```
CREATE DATABASE [IF NOT EXISTS] test_database;
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testpassword';
GRANT ALL ON test_database.* TO 'testuser'@'localhost';
```