
from database import Database

db = Database()
try:
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1;")
    result = cursor.fetchone()
    if result:
        print(" Database is connected!")
    cursor.close()
    db.return_connection(conn)
except Exception as e:
    print(f" Connection failed: {e}")