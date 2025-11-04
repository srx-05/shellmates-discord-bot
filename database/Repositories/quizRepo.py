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
