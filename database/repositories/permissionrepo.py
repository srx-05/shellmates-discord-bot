from database.connection import Database

class permissionrepo:
    def __init__(self, db_manager: Database):
        self.db = db_manager

    def add_permission(self, admin_id, module, can_create=False, can_read=True, can_update=False, can_delete=False):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO permissions (admin_id, module, can_create, can_read, can_update, can_delete)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (admin_id, module) DO UPDATE
                    SET can_create=EXCLUDED.can_create,
                        can_read=EXCLUDED.can_read,
                        can_update=EXCLUDED.can_update,
                        can_delete=EXCLUDED.can_delete
                    RETURNING id
                    """,
                    (admin_id, module, can_create, can_read, can_update, can_delete)
                )
                permission_id = cur.fetchone()[0]
                conn.commit()
                return permission_id
        except Exception as e:
            conn.rollback()
            print(f"❌ Error adding permission: {e}")
            return None
        finally:
            self.db.return_connection(conn)