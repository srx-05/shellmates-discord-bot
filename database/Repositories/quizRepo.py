from database.connection import Database

class QuizRepository:
    @staticmethod
    def create_quiz(fact_id, question, correct_answer, wrong_answers, difficulty='medium'):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO quiz (fact_id, question, correct_answer, wrong_answers, difficulty)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *;
        """, (fact_id, question, correct_answer, wrong_answers, difficulty))

        quiz = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return quiz

    @staticmethod
    def get_all_quizzes():
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM quiz;")
        quizzes = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return quizzes

    @staticmethod
    def delete_quiz(quiz_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM quiz WHERE quiz_id = %s;", (quiz_id,))
        conn.commit()
        cur.close()
        db.return_connection(conn)


#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------


    @staticmethod
    def get_quiz(quiz_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM quiz WHERE quiz_id = %s;", (quiz_id,))
        quiz = cur.fetchone()
        cur.close()
        db.return_connection(conn)
        return quiz

    @staticmethod
    def update_quiz(quiz_id, question=None, correct_answer=None, wrong_answers=None, difficulty=None):
        """
        Update provided fields (pass None to leave unchanged). Returns updated row.
        """
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE quiz
            SET question = COALESCE(%s, question),
                correct_answer = COALESCE(%s, correct_answer),
                wrong_answers = COALESCE(%s, wrong_answers),
                difficulty = COALESCE(%s, difficulty)
            WHERE quiz_id = %s
            RETURNING *;
        """, (question, correct_answer, wrong_answers, difficulty, quiz_id))
        updated = cur.fetchone()
        conn.commit()
        cur.close()
        db.return_connection(conn)
        return updated

    @staticmethod
    def get_quizzes_by_difficulty(difficulty, limit=50, offset=0):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM quiz WHERE difficulty = %s ORDER BY quiz_id DESC LIMIT %s OFFSET %s;",
                    (difficulty, limit, offset))
        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return rows

    @staticmethod
    def get_quizzes_for_fact(fact_id):
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM quiz WHERE fact_id = %s;", (fact_id,))
        rows = cur.fetchall()
        cur.close()
        db.return_connection(conn)
        return rows

    @staticmethod
    def fetch_random_quiz(difficulty=None):
        """Return a single random quiz, optionally filtered by difficulty."""
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        if difficulty:
            cur.execute("SELECT * FROM quiz WHERE difficulty = %s ORDER BY RANDOM() LIMIT 1;", (difficulty,))
        else:
            cur.execute("SELECT * FROM quiz ORDER BY RANDOM() LIMIT 1;")
        row = cur.fetchone()
        cur.close()
        db.return_connection(conn)
        return row

    @staticmethod
    def check_answer(quiz_id, answer):
        """
        Return True if answer matches correct_answer (case-insensitive, stripped), else False.
        """
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT correct_answer FROM quiz WHERE quiz_id = %s;", (quiz_id,))
        row = cur.fetchone()
        cur.close()
        db.return_connection(conn)
        if not row:
            return False
        correct = row[0]
        if correct is None:
            return False
        return str(correct).strip().lower() == str(answer).strip().lower()

    @staticmethod
    def count_quizzes():
        db = Database()
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM quiz;")
        cnt = cur.fetchone()[0]
        cur.close()
        db.return_connection(conn)
        return cnt
