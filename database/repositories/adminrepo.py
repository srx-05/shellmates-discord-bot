from database.connection import Database

class adminrepo:
    def __init__(self, db_manager: Database):
        self.db = db_manager

    def add_admin(self, user_id, role='moderator'):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO admins (user_id, role)
                    VALUES (%s, %s)
                    ON CONFLICT (user_id) DO UPDATE
                    SET role = EXCLUDED.role
                    RETURNING id
                    """,
                    (user_id, role)
                )
                admin_id = cur.fetchone()[0]
                conn.commit()
                return admin_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Error adding admin: {e}")
            return None
        finally:
            self.db.return_connection(conn)

    def get_admin_by_user_id(self, user_id):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, user_id, role, added_at, is_active FROM admins WHERE user_id = %s",
                    (user_id,)
                )
                result = cur.fetchone()
                if result:
                    return {
                        'id': result[0],
                        'user_id': result[1],
                        'role': result[2],
                        'added_at': result[3],
                        'is_active': result[4]
                    }
                return None
        finally:
            self.db.return_connection(conn)