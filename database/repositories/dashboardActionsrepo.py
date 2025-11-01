from database.connection import Database

class dashboardActionsrepo:
    def __init__(self, db_manager: Database):
        self.db = db_manager

    def add_action(self, admin_id, action, target_table=None, target_id=None, ip_address=None, details=None):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO dashboard_actions (admin_id, action, target_table, target_id, ip_address, details)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (admin_id, action, target_table, target_id, ip_address, details)
                )
                action_id = cur.fetchone()[0]
                conn.commit()
                return action_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Error adding dashboard action: {e}")
            return None
        finally:
            self.db.return_connection(conn)