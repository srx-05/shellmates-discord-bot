from database.connection import Database

class annoucementsrepo:
    def __init__(self, db_manager: Database):
        self.db = db_manager

    def add_announcement(self, title, message, sent_by, is_pinned=False):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO announcements (title, message, sent_by, is_pinned)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (title, message, sent_by, is_pinned)
                )
                ann_id = cur.fetchone()[0]
                conn.commit()
                return ann_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Error adding announcement: {e}")
            return None
        finally:
            self.db.return_connection(conn)