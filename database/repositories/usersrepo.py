


class UserRepository:
    """مستودع المستخدمين - للتعامل مع جدول users"""

    def __init__(self, db_manager):
        self.db = db_manager

    def add_user(self, discord_id, username):
        """إضافة مستخدم جديد"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (discord_id, username)
                    VALUES (%s, %s)
                    ON CONFLICT (discord_id) DO UPDATE 
                    SET username = EXCLUDED.username
                    RETURNING id
                    """,
                    (discord_id, username)
                )
                user_id = cur.fetchone()[0]
                conn.commit()
                return user_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Error adding user: {e}")
            return None
        finally:
            self.db.return_connection(conn)

    def get_user_by_discord_id(self, discord_id):
        """البحث عن مستخدم بواسطة Discord ID"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, discord_id, username, joined_at, created_at
                    FROM users
                    WHERE discord_id = %s
                    """,
                    (discord_id,)
                )
                result = cur.fetchone()
                if result:
                    return {
                        'id': result[0],
                        'discord_id': result[1],
                        'username': result[2],
                        'joined_at': result[3],
                        'created_at': result[4]
                    }
                return None
        finally:
            self.db.return_connection(conn)

    def get_all_users(self, limit=100, offset=0):
        """الحصول على جميع المستخدمين مع Pagination"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, discord_id, username, joined_at
                    FROM users
                    ORDER BY joined_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (limit, offset)
                )
                return cur.fetchall()
        finally:
            self.db.return_connection(conn)

    def update_username(self, user_id, new_username):
        """تحديث اسم المستخدم"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET username = %s
                    WHERE id = %s
                    RETURNING id
                    """,
                    (new_username, user_id)
                )
                conn.commit()
                return cur.fetchone() is not None
        except Exception as e:
            conn.rollback()
            print(f"❌ Error updating username: {e}")
            return False
        finally:
            self.db.return_connection(conn)

    def delete_user(self, user_id):
        """حذف مستخدم"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"❌ Error deleting user: {e}")
            return False
        finally:
            self.db.return_connection(conn)
