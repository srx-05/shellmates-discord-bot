# database/connection.py
import asyncpg
from config import Config
import logging

logger = logging.getLogger(__name__)

class PostgreSQL:
    _pool = None

    @classmethod
    async def connect(cls):
        if cls._pool is None:
            try:
                cls._pool = await asyncpg.create_pool(dsn=Config.DATABASE_URL)
                logger.info("✓ Connected to PostgreSQL")
            except Exception as e:
                logger.error(f"✗ Failed to connect to PostgreSQL: {e}")
                raise
        return cls._pool

    @classmethod
    async def close(cls):
        if cls._pool:
            await cls._pool.close()
            logger.info("✓ PostgreSQL connection closed")
            cls._pool = None

    @classmethod
    async def fetch(cls, query, *args):
        if cls._pool is None:
            await cls.connect()
        async with cls._pool.acquire() as conn:
            return await conn.fetch(query, *args)

    @classmethod
    async def execute(cls, query, *args):
        if cls._pool is None:
            await cls.connect()
        async with cls._pool.acquire() as conn:
            await conn.execute(query, *args)


# global alias
db = PostgreSQL
