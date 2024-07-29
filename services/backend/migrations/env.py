import os
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from alembic import context
from models.user import *
from models.advertisment import *
import asyncio

config = context.config
fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

DB_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres')


def run_migrations_offline():

    url = DB_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():

    connectable = create_async_engine(DB_URL, echo=True, future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())