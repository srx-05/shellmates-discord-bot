from database.connection import Database

class PointsRepository:
    @staticmethod
    def add_points(user_id, reason, points_added):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO points_history (user_id, reason, points_added)
            VALUES (%s, %s, %s)
            RETURNING *;
        """, (user_id, reason, points_added))

        record = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return record

    @staticmethod
    def get_points_history(user_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM points_history WHERE user_id = %s;", (user_id,))
        records = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return records
