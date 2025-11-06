from database.connection import Database
import re


class BannedWordRepository:
    @staticmethod
    def add_banned_word(word):
        """Add a new banned word to the database."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO banned_words (word)
            VALUES (%s)
            RETURNING *;
            """,
            (word,),
        )

        new_word = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return new_word

    # ----------------------------------------------------------------------

    @staticmethod
    def get_all_banned_words():
        """Return all banned words."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM banned_words ORDER BY created_at DESC;")
        words = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return words

    # ----------------------------------------------------------------------

    @staticmethod
    def delete_banned_word(word):
        """Delete a banned word by text (case-insensitive)."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM banned_words WHERE LOWER(word) = LOWER(%s);", (word,))
        conn.commit()
        cur.close()
        db.return_connection(conn)

    # ----------------------------------------------------------------------

    @staticmethod
    def get_banned_word(word):
        """Return the banned_words row matching `word` (case-insensitive) or None."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM banned_words WHERE LOWER(word) = LOWER(%s) LIMIT 1;",
            (word,),
        )
        row = cur.fetchone()
        cur.close()
        db.return_connection(conn)
        return row

    # ----------------------------------------------------------------------

    @staticmethod
    def exists_banned_word(word):
        """Return True if the word is present in the banned list (case-insensitive)."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM banned_words WHERE LOWER(word) = LOWER(%s) LIMIT 1;",
            (word,),
        )
        found = cur.fetchone() is not None
        cur.close()
        db.return_connection(conn)
        return found

    # ----------------------------------------------------------------------

    @staticmethod
    def update_banned_word(old_word, new_word=None):
        """
        Update a banned word entry (case-insensitive on old_word).
        Returns the updated row.
        """
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE banned_words
            SET word = COALESCE(%s, word)
            WHERE LOWER(word) = LOWER(%s)
            RETURNING *;
            """,
            (new_word, old_word),
        )
        updated = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return updated

    # ----------------------------------------------------------------------

    @staticmethod
    def find_banned_words_in_text(text):
        """
        Return a list of banned words found in `text`.
        Matching is case-insensitive and uses word-boundary matching (\b).
        """
        if not text:
            return []

        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT word FROM banned_words;")
        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)

        found = set()
        for (w,) in rows:
            if not w:
                continue
            pattern = r"\b" + re.escape(w) + r"\b"
            if re.search(pattern, text, flags=re.IGNORECASE):
                found.add(w)
        return list(found)
