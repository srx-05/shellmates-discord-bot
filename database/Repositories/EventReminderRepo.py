from database.connection import Database


class ReminderRepository:
    @staticmethod
    def create_table():
        """Create the reminders table if it doesn't exist."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS event_reminders (
                reminder_id BIGSERIAL PRIMARY KEY,
                event_id BIGINT REFERENCES events(event_id) ON DELETE CASCADE,
                remind_before INTEGER,
                sent BOOLEAN DEFAULT FALSE
            );
        """
        )

        conn.commit()
        cur.close()
        db.return_connection(conn)

    # --------------------------------------------------------------------------
    @staticmethod
    def add_reminder_for_event(event_id, remind_before=60):
        """Add a default reminder before the event."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO event_reminders (event_id, remind_before)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """,
            (event_id, remind_before),
        )

        conn.commit()
        cur.close()
        db.return_connection(conn)

    # --------------------------------------------------------------------------
    @staticmethod
    def get_pending_reminders():
        """Fetch reminders that should be sent now."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT r.reminder_id, e.event_id, e.title, e.event_date, e.channel_id, r.remind_before
            FROM event_reminders r
            JOIN events e ON e.event_id = r.event_id
            WHERE r.sent = FALSE
              AND (e.event_date - (r.remind_before || ' minutes')::INTERVAL) <= NOW()
              AND e.event_date > NOW();
        """
        )

        reminders = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return reminders

    # --------------------------------------------------------------------------
    @staticmethod
    def mark_as_sent(reminder_id):
        """Mark reminder as sent."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE event_reminders SET sent = TRUE WHERE reminder_id = %s;",
            (reminder_id,),
        )
        conn.commit()
        cur.close()
        db.return_connection(conn)
