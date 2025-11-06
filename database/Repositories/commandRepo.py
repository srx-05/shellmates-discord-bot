from database.connection import Database


class CommandRepository:
    @staticmethod
    def create_command(command_name, description, category="General"):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO commands (command_name, description, category)
            VALUES (%s, %s, %s)
            RETURNING *;
        """,
            (command_name, description, category),
        )

        command = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return command

    @staticmethod
    def get_all_commands():
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM commands;")
        commands = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return commands

    # @staticmethod
    # def increment_usage(command_name):
    #     db = Database()
    #     conn = db.get_connection()
    #     cur = conn.cursor()

    #     cur.execute("""
    #         UPDATE commands
    #         SET usage_count = usage_count + 1,
    #             last_used = CURRENT_TIMESTAMP
    #         WHERE command_name = %s
    #         RETURNING *;
    #     """, (command_name,))

    #     updated_command = cur.fetchone()
    #     conn.commit()
    #     cur.close()
    #     db.return_connection(conn)
    #     return updated_command

    @staticmethod
    def delete_command(command_name):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM commands WHERE command_name = %s;", (command_name,))
        conn.commit()
        cur.close()
        db.return_connection(conn)

    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------

    @staticmethod
    def get_command(command_name):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM commands WHERE command_name = %s;", (command_name,))
        cmd = cur.fetchone()
        cur.close()
        db.return_connection(conn)
        return cmd

    @staticmethod
    def update_command(command_name, description=None, enabled=None, category=None):
        """
        Update provided fields (pass None to leave unchanged). Returns updated row.
        """
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE commands
            SET description = COALESCE(%s, description),
                enabled = COALESCE(%s, enabled),
                category = COALESCE(%s, category)
            WHERE command_name = %s
            RETURNING *;
        """,
            (description, enabled, category, command_name),
        )
        updated = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return updated

    # @staticmethod
    # def get_top_commands(limit=10):
    #     """Return commands ordered by usage_count desc."""
    #     db = Database()
    #     conn = db.get_connection()
    #     cur = conn.cursor()
    #     cur.execute("""
    #         SELECT command_name, usage_count
    #         FROM commands
    #         ORDER BY COALESCE(usage_count, 0) DESC
    #         LIMIT %s;
    #     """, (limit,))
    #     rows = cur.fetchall()
    #     cur.close()
    #     db.return_connection(conn)
    #     return rows

    @staticmethod
    def search_commands(term, limit=50, offset=0):
        """Simple search on command_name and description."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        like = f"%{term}%"
        cur.execute(
            """
            SELECT * FROM commands
            WHERE command_name ILIKE %s OR description ILIKE %s
            ORDER BY command_name ASC
            LIMIT %s OFFSET %s;
        """,
            (like, like, limit, offset),
        )
        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return rows

    @staticmethod
    def command_exists(name: str) -> bool:
        return CommandRepository.get_command(name) is not None
