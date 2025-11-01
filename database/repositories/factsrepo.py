class CyberFactsRepository:
    """مستودع الحقائق السيبرانية"""

    def __init__(self, db_manager):
        self.db = db_manager

    def add_fact(self, fact, category, added_by):
        """إضافة حقيقة جديدة"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO cyber_facts (fact, category, added_by)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (fact, category, added_by)
                )
                fact_id = cur.fetchone()[0]
                conn.commit()
                return fact_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Error adding fact: {e}")
            return None
        finally:
            self.db.return_connection(conn)

    def approve_fact(self, fact_id, approved_by):
        """الموافقة على حقيقة"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE cyber_facts
                    SET approved = TRUE, 
                        approved_at = CURRENT_TIMESTAMP,
                        approved_by = %s
                    WHERE id = %s
                    """,
                    (approved_by, fact_id)
                )
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"❌ Error approving fact: {e}")
            return False
        finally:
            self.db.return_connection(conn)

    def get_random_approved_fact(self):
        """الحصول على حقيقة عشوائية موافق عليها"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, fact, category
                    FROM cyber_facts
                    WHERE approved = TRUE
                    ORDER BY RANDOM()
                    LIMIT 1
                    """
                )
                return cur.fetchone()
        finally:
            self.db.return_connection(conn)

    def get_pending_facts(self):
        """الحصول على الحقائق التي تحتاج موافقة"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT cf.id, cf.fact, cf.category, 
                           u.username, cf.added_at
                    FROM cyber_facts cf
                    JOIN users u ON cf.added_by = u.id
                    WHERE cf.approved = FALSE
                    ORDER BY cf.added_at ASC
                    """
                )
                return cur.fetchall()
        finally:
            self.db.return_connection(conn)
