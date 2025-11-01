class EventRepository:
    """مستودع الأحداث"""

    def __init__(self, db_manager):
        self.db = db_manager

    def create_event_with_reminders(self, title, description, event_date,
                                    location, created_by):
        """إنشاء حدث مع تذكيرات تلقائية"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                # استخدام الـ Stored Procedure
                cur.execute(
                    """
                    SELECT create_event_with_reminders(%s, %s, %s, %s, %s)
                    """,
                    (title, description, event_date, location, created_by)
                )
                event_id = cur.fetchone()[0]
                conn.commit()
                return event_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Error creating event: {e}")
            return None
        finally:
            self.db.return_connection(conn)

    def get_upcoming_events(self):
        """الحصول على الأحداث القادمة من الـ View"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM upcoming_events")
                columns = [desc[0] for desc in cur.description]
                results = []
                for row in cur.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
        finally:
            self.db.return_connection(conn)

    def register_attendance(self, event_id, user_id, status):
        """تسجيل حضور لحدث"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT register_event_attendance(%s, %s, %s)
                    """,
                    (event_id, user_id, status)
                )
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"❌ Error registering attendance: {e}")
            return False
        finally:
            self.db.return_connection(conn)

    def get_event_attendees(self, event_id):
        """الحصول على قائمة الحاضرين لحدث"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT u.id, u.username, ea.status, ea.responded_at
                    FROM event_attendance ea
                    JOIN users u ON ea.user_id = u.id
                    WHERE ea.event_id = %s
                    ORDER BY ea.responded_at DESC
                    """,
                    (event_id,)
                )
                return cur.fetchall()
        finally:
            self.db.return_connection(conn)
