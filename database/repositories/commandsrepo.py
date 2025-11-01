class CommandLogger:
    """تسجيل استخدام الأوامر"""

    def __init__(self, db_manager):
        self.db = db_manager

    def log_command(self, user_id, command_name, parameters=None,
                    success=True, error_message=None):
        """تسجيل استخدام أمر"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO commands_log 
                    (user_id, command_name, parameters, success, error_message)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (user_id, command_name, parameters, success, error_message)
                )
                conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"❌ Error logging command: {e}")
        finally:
            self.db.return_connection(conn)

    def get_command_statistics(self):
        """الحصول على إحصائيات الأوامر"""
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM command_statistics LIMIT 20")
                return cur.fetchall()
        finally:
            self.db.return_connection(conn)

