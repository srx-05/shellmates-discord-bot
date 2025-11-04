from database.connection import Database


class PointsRepository:
    @staticmethod
    def add_points(user_id, reason, points):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO points_history (user_id, reason, points_added)
            VALUES (%s, %s, %s)
            RETURNING *;
        """, (user_id, reason, points))
        record = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return record

    @staticmethod
    def get_history(user_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM points_history WHERE user_id = %s ORDER BY created_at DESC;", (user_id,))
        history = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return history


class FactRepository:
    @staticmethod
    def add_fact(content, source_type, source_url, added_by):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO cyber_facts (content, source_type, source_url, added_by)
            VALUES (%s, %s, %s, %s)
            RETURNING *;
        """, (content, source_type, source_url, added_by))
        fact = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return fact

    @staticmethod
    def get_random_fact():
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cyber_facts ORDER BY RANDOM() LIMIT 1;")
        fact = cur.fetchone()
        cur.close()
        db.return_connection(conn)
        return fact
