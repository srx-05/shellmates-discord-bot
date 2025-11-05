from database.connection import Database

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


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

    @staticmethod
    def get_fact(fact_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cyber_facts WHERE fact_id = %s;", (fact_id,))
        row = cur.fetchone()
        cur.close()
        db.return_connection(conn)
        return row

    @staticmethod
    def get_facts(limit=50, offset=0):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cyber_facts ORDER BY fact_id DESC LIMIT %s OFFSET %s;", (limit, offset))
        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return rows

    @staticmethod
    def get_facts_by_user(added_by, limit=50, offset=0):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cyber_facts WHERE added_by = %s ORDER BY fact_id DESC LIMIT %s OFFSET %s;",
                    (added_by, limit, offset))
        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return rows

    @staticmethod
    def update_fact(fact_id, content=None, source_type=None, source_url=None):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE cyber_facts
            SET content = COALESCE(%s, content),
                source_type = COALESCE(%s, source_type),
                source_url = COALESCE(%s, source_url)
            WHERE fact_id = %s
            RETURNING *;
        """, (content, source_type, source_url, fact_id))
        updated = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return updated

    @staticmethod
    def delete_fact(fact_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM cyber_facts WHERE fact_id = %s;", (fact_id,))
        conn.commit()
        cur.close()
        db.return_connection(conn)

    @staticmethod
    def search_facts(term, limit=50, offset=0):
        """Simple full-text LIKE search on content. Use proper full-text search in production."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        like = f"%{term}%"
        cur.execute("SELECT * FROM cyber_facts WHERE content ILIKE %s ORDER BY fact_id DESC LIMIT %s OFFSET %s;",
                    (like, limit, offset))
        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return rows

    @staticmethod
    def count_facts():
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM cyber_facts;")
        cnt = cur.fetchone()[0]
        cur.close()
        db.return_connection(conn)
        return int(cnt)
