# CYSL Web Backend

## Database Migrations

### Alembic Init

So I remember how to setup async database and `migrations` directory

`alembic init -t async migrations`

Update `migrations/script.py.mako` section
```
from alembic import op
import sqlalchemy as sa
import sqlmodel         #NEW
```

Update `migrations/env.py`:
```
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel                       # NEW

from alembic import context

from app.models import Season, Misconduct      # noqa
```

Replace line `target_metadata = None` with `target_metadata = SQLModel.metadata` 

Update `alembic.ini`

Replace line `sqlalchemy.url = driver://user:pass@localhost/dbname` with
`sqlalchemy.url = postgresql+asyncpg://user:pass@localhost/dbname`

### Generating Migrations

```
alembic revision --autogenerate
```

### Applying Migrations

```
alembic upgrade head
```

