import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        """إنشاء Connection Pool"""
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
            print("✅ Connection pool created successfully")
        except Exception as e:
            print(f"❌ Error creating connection pool: {e}")
            raise

    def get_connection(self):
        """الحصول على اتصال من الـ Pool"""
        return self.connection_pool.getconn()

    def return_connection(self, connection):
        """إرجاع الاتصال إلى الـ Pool"""
        self.connection_pool.putconn(connection)

    def close_all_connections(self):
        """إغلاق جميع الاتصالات"""
        self.connection_pool.closeall()
        print("✅ All connections closed")