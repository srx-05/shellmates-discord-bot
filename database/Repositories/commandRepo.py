from database.connection import Database

class CommandRepository:
    @staticmethod
    def create_command(command_name, description):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO commands (command_name, description)
            VALUES (%s, %s)
            RETURNING *;
        """, (command_name, description))

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

    @staticmethod
    def increment_usage(command_name):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE commands
            SET usage_count = usage_count + 1,
                last_used = CURRENT_TIMESTAMP
            WHERE command_name = %s
            RETURNING *;
        """, (command_name,))

        updated_command = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return updated_command

    @staticmethod
    def delete_command(command_name):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM commands WHERE command_name = %s;", (command_name,))
        conn.commit()
        cur.close()
        db.return_connection(conn)
