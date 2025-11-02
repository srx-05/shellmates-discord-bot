<<<<<<< HEAD
import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):

        try:
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=int(os.getenv('DB_POOL_MIN', 5)),
                maxconn=int(os.getenv('DB_POOL_MAX', 20)),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            print(" Connection pool created successfully")
        except Exception as e:
            print(f" Error creating connection pool: {e}")
            raise

    def get_connection(self):
        return self.connection_pool.getconn()

    def return_connection(self, connection):

        self.connection_pool.putconn(connection)

    def close_all_connections(self):

        self.connection_pool.closeall()
        print(" All connections closed")
=======
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
>>>>>>> 36ff42c9ed8b445e4801c64da9cf4affda811436
