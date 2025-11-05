from database.connection import Database

class UserRepository:
    @staticmethod
    def create_user(user_id, username, role='member'):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (user_id, username, role)
            VALUES (%s, %s, %s)
            RETURNING *;
        """, (user_id, username, role))

        user = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return user

    @staticmethod
    def get_all_users():
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users;")
        users = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return users

    @staticmethod
    def delete_user(user_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE user_id = %s;", (user_id,))
        conn.commit()
        cur.close()
        db.return_connection(conn)

        
    @staticmethod
    def update_user(user_id, username=None, role=None):
        """
        Update username and/or role. Pass None to leave a field unchanged.
        Returns the updated row.
        """
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE users
            SET username = COALESCE(%s, username),
                role = COALESCE(%s, role)
            WHERE user_id = %s
            RETURNING *;
        """, (username, role, user_id))

        updated = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return updated
