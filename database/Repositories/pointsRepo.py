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


# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

    @staticmethod
    def get_total_points(user_id):
        """Return the sum of points for a user (int)."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COALESCE(SUM(points_added), 0) FROM points_history WHERE user_id = %s;", (user_id,))
        total = cur.fetchone()[0]
        cur.close()
        db.return_connection(conn)
        return int(total)

    @staticmethod
    def get_recent_history(user_id, limit=10):
        """Return most recent point history rows for a user."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM points_history WHERE user_id = %s ORDER BY created_at DESC LIMIT %s;",
                    (user_id, limit))
        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return rows

    @staticmethod
    def get_leaderboard(limit=10):
        """Return list of (user_id, total_points) ordered desc."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT user_id, COALESCE(SUM(points_added),0) AS total
            FROM points_history
            GROUP BY user_id
            ORDER BY total DESC
            LIMIT %s;
        """, (limit,))
        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return rows

    @staticmethod
    def deduct_points(user_id, reason, points):
        """Insert a negative points entry (use positive `points`, will be negated)."""
        return PointsRepository.add_points(user_id, reason, -abs(points))
