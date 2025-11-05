from database.connection import db
import os

def execute_sql_file(file_path):
    conn = db.get_connection()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            sql_commands = f.read()

        with conn.cursor() as cursor:
            cursor.execute(sql_commands)
            conn.commit()
            print("✅ Database schema created successfully!")

    except Exception as e:
        print(f"❌ Error while creating tables: {e}")
        conn.rollback()  # optional but recommended
    finally:
        db.return_connection(conn)


if __name__ == "__main__":
    sql_file = os.path.join(os.path.dirname(__file__), "schema.sql")
    execute_sql_file(sql_file)
