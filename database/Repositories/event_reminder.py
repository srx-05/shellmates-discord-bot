import datetime
import time
import threading
from database.connection import Database


class EventReminder:
    def __init__(self, check_interval=60):
        """
        check_interval: how often to check reminders (in seconds)
        """
        self.check_interval = check_interval
        self.running = False

    # --------------------------------------------------------------------------
    def start(self):
        """Start the reminder loop in a background thread."""
        self.running = True
        print(" Event reminder service started.")
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        """Stop the reminder loop."""
        self.running = False
        print("⏹️ Event reminder service stopped.")

    # --------------------------------------------------------------------------
    def _loop(self):
        """Main loop that checks for reminders to send."""
        while self.running:
            try:
                self.check_and_send_reminders()
            except Exception as e:
                print(f" Error in reminder loop: {e}")
            time.sleep(self.check_interval)

    # --------------------------------------------------------------------------
    @staticmethod
    def check_and_send_reminders():
        """Fetch reminders that should be sent now and mark them as sent."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        # Current UTC time
        now = datetime.datetime.utcnow()

        # SQL query: find reminders not sent yet, and the event time minus remind_before <= now
        cur.execute("""
            SELECT r.reminder_id, r.event_id, r.user_id, e.title, e.event_date, r.remind_before
            FROM event_reminders r
            JOIN events e ON r.event_id = e.event_id
            WHERE r.sent = FALSE
              AND (e.event_date - (r.remind_before || ' minutes')::INTERVAL) <= NOW()
              AND e.event_date > NOW();
        """)

        reminders_to_send = cur.fetchall()

        for reminder in reminders_to_send:
            reminder_id, event_id, user_id, title, event_date, remind_before = reminder

            #  Send the reminder 
            print(f" Reminder for user {user_id}: '{title}' starts at {event_date} (in {remind_before} min)")

            # Mark as sent
            cur.execute("UPDATE event_reminders SET sent = TRUE WHERE reminder_id = %s;", (reminder_id,))

        conn.commit()
        cur.close()
        db.return_connection(conn)

    # --------------------------------------------------------------------------
    @staticmethod
    def add_reminder(event_id, user_id, remind_before=10):
        """Add a new reminder for a specific user/event."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO event_reminders (event_id, user_id, remind_before)
            VALUES (%s, %s, %s)
            RETURNING reminder_id;
        """, (event_id, user_id, remind_before))

        reminder_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return reminder_id

    # --------------------------------------------------------------------------
    @staticmethod
    def get_user_reminders(user_id, sent_only=False):
        """Fetch all reminders for a given user."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        if sent_only:
            cur.execute("""
                SELECT r.*, e.title, e.event_date
                FROM event_reminders r
                JOIN events e ON r.event_id = e.event_id
                WHERE r.user_id = %s AND r.sent = TRUE
                ORDER BY e.event_date DESC;
            """, (user_id,))
        else:
            cur.execute("""
                SELECT r.*, e.title, e.event_date
                FROM event_reminders r
                JOIN events e ON r.event_id = e.event_id
                WHERE r.user_id = %s
                ORDER BY e.event_date ASC;
            """, (user_id,))

        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return rows
