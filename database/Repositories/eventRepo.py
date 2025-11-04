from database.connection import Database

class EventRepository:
    @staticmethod
    def create_event(title, description, event_date, created_by, channel_id, message_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO events (title, description, event_date, created_by, channel_id, message_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *;
        """, (title, description, event_date, created_by, channel_id, message_id))

        event = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return event

    @staticmethod
    def get_upcoming_events():
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM events WHERE event_date > NOW() ORDER BY event_date ASC;")
        events = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return events

    @staticmethod
    def delete_event(event_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM events WHERE event_id = %s;", (event_id,))
        conn.commit()
        cur.close()
        db.return_connection(conn)
