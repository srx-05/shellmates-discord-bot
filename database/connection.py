from psycopg2 import pool
from config import Config 
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):

        try:
            self.connection_pool = pool.ThreadedConnectionPool(
                minconn=Config.DB_POOL_MIN,
                maxconn=Config.DB_POOL_MAX,
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
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


db = Database()