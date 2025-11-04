from database.connection import Database

class BannedWordRepository:
    @staticmethod
    def add_banned_word(word, added_by):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO banned_words (word, added_by)
            VALUES (%s, %s)
            RETURNING *;
        """, (word, added_by))

        new_word = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return new_word

    @staticmethod
    def get_all_banned_words():
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM banned_words;")
        words = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return words

    @staticmethod
    def delete_banned_word(word):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM banned_words WHERE word = %s;", (word,))
        conn.commit()
        cur.close()
        db.return_connection(conn)
