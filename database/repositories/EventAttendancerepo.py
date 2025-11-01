from database.connection import Database

class EventAttendancerepo:
    def __init__(self, db_manager: Database):
        self.db = db_manager

    def add_attendance(self, event_id, user_id, status='pending'):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO event_attendance (event_id, user_id, status)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (event_id, user_id) DO UPDATE
                    SET status = EXCLUDED.status
                    RETURNING id
                    """,
                    (event_id, user_id, status)
                )
                attendance_id = cur.fetchone()[0]
                conn.commit()
                return attendance_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Error adding attendance: {e}")
            return None
        finally:
            self.db.return_connection(conn)