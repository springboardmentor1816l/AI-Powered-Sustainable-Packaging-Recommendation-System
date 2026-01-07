from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from backend.app import create_app
from backend.extensions import db

# Alembic Config object
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🔑 IMPORTANT: metadata
target_metadata = db.metadata


def run_migrations_online():
    app = create_app()

    with app.app_context():
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True
            )

            with context.begin_transaction():
                context.run_migrations()
