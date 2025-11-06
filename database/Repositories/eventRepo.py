from database.connection import Database


class EventRepository:
    @staticmethod
    def create_event(
        title, description, event_date, created_by, channel_id, message_id
    ):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO events (title, description, event_date, created_by, channel_id, message_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *;
        """,
            (title, description, event_date, created_by, channel_id, message_id),
        )

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
        cur.execute(
            "SELECT * FROM events WHERE event_date > NOW() ORDER BY event_date ASC;"
        )
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

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    @staticmethod
    def get_event(event_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM events WHERE event_id = %s;", (event_id,))
        row = cur.fetchone()
        cur.close()
        db.return_connection(conn)
        return row

    @staticmethod
    def update_event(
        event_id,
        title=None,
        description=None,
        event_date=None,
        channel_id=None,
        message_id=None,
    ):
        """
        Update any provided fields (pass None to leave unchanged). Returns updated row.
        """
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE events
            SET title = COALESCE(%s, title),
                description = COALESCE(%s, description),
                event_date = COALESCE(%s, event_date),
                channel_id = COALESCE(%s, channel_id),
                message_id = COALESCE(%s, message_id)
            WHERE event_id = %s
            RETURNING *;
        """,
            (title, description, event_date, channel_id, message_id, event_id),
        )
        updated = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return updated

    @staticmethod
    def get_events_by_channel(channel_id, upcoming_only=True, limit=50, offset=0):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        if upcoming_only:
            cur.execute(
                """
                SELECT * FROM events
                WHERE channel_id = %s AND event_date > NOW()
                ORDER BY event_date ASC
                LIMIT %s OFFSET %s;
            """,
                (channel_id, limit, offset),
            )
        else:
            cur.execute(
                """
                SELECT * FROM events
                WHERE channel_id = %s
                ORDER BY event_date DESC
                LIMIT %s OFFSET %s;
            """,
                (channel_id, limit, offset),
            )
        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return rows

    @staticmethod
    def get_events_by_creator(created_by, upcoming_only=True, limit=50, offset=0):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        if upcoming_only:
            cur.execute(
                """
                SELECT * FROM events
                WHERE created_by = %s AND event_date > NOW()
                ORDER BY event_date ASC
                LIMIT %s OFFSET %s;
            """,
                (created_by, limit, offset),
            )
        else:
            cur.execute(
                """
                SELECT * FROM events
                WHERE created_by = %s
                ORDER BY event_date DESC
                LIMIT %s OFFSET %s;
            """,
                (created_by, limit, offset),
            )
        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return rows

    @staticmethod
    def get_past_events(limit=50, offset=0):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM events WHERE event_date <= NOW() ORDER BY event_date DESC LIMIT %s OFFSET %s;",
            (limit, offset),
        )
        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return rows
