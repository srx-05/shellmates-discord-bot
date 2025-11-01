from database.connection import Database

class reactionrepo:
    def __init__(self, db_manager: Database):
        self.db = db_manager

    def add_reaction(self, user_id, message_id, reaction):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO reactions (user_id, message_id, reaction)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id, message_id, reaction) DO NOTHING
                    RETURNING id
                    """,
                    (user_id, message_id, reaction)
                )
                reaction_id = cur.fetchone()
                conn.commit()
                return reaction_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Error adding reaction: {e}")
            return None
        finally:
            self.db.return_connection(conn)