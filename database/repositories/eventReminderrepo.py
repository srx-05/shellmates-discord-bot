from database.connection import Database

class eventReminderrepo:
    def __init__(self, db_manager: Database):
        self.db = db_manager

    def add_reminder(self, event_id, user_id, reminder_time, type='pre-event', sent=False):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO event_reminders (event_id, user_id, reminder_time, type, sent)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (event_id, user_id, reminder_time, type, sent)
                )
                reminder_id = cur.fetchone()[0]
                conn.commit()
                return reminder_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Error adding reminder: {e}")
            return None
        finally:
            self.db.return_connection(conn)