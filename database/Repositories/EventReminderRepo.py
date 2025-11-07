from database.connection import Database
from datetime import datetime


class ReminderRepository:
    @staticmethod
    def get_pending_reminders():
        """Fetch reminders that should be sent now."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT r.reminder_id, e.event_id, e.title, e.event_date, r.user_id, r.remind_before
            FROM event_reminders r
            JOIN events e ON e.event_id = r.event_id
            WHERE r.sent = FALSE
              AND (e.event_date - (r.remind_before || ' minutes')::INTERVAL) <= NOW()
              AND e.event_date > NOW() - INTERVAL '1 hour';  -- Added buffer for past events
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

    # --------------------------------------------------------------------------
    @staticmethod
    def add_reminder_for_event(event_id, user_id, remind_before=60):
        """Add a reminder for a specific user."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO event_reminders (event_id, user_id, remind_before)
            VALUES (%s, %s, %s);
            """,
            (event_id, user_id, remind_before),
        )

        conn.commit()
        cur.close()
        db.return_connection(conn)

    # --------------------------------------------------------------------------
    @staticmethod
    def get_user_reminders(user_id):
        """Get all reminders for a specific user."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT r.reminder_id, e.title, e.event_date, r.remind_before, r.sent,
                   (e.event_date <= NOW()) as is_past
            FROM event_reminders r
            JOIN events e ON e.event_id = r.event_id
            WHERE r.user_id = %s
            ORDER BY e.event_date;
            """,
            (user_id,),
        )

        reminders = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return reminders

    # --------------------------------------------------------------------------
    @staticmethod
    def cleanup_expired_reminders():
        """Mark reminders as sent for events that are more than 1 hour past."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE event_reminders 
            SET sent = TRUE 
            WHERE sent = FALSE 
            AND event_id IN (
                SELECT event_id FROM events 
                WHERE event_date <= NOW() - INTERVAL '1 hour'
            );
            """
        )

        cleaned_count = cur.rowcount
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return cleaned_count
