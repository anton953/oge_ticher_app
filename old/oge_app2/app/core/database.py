import sqlite3

class Database:
    def __init__(self, path="data/app.db"):
        self.conn = sqlite3.connect(path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            topic TEXT,
            correct INTEGER,
            total INTEGER
        )
        """)

        self.conn.commit()

    def update_progress(self, topic, correct, total):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO progress VALUES (?, ?, ?)",
            (topic, correct, total)
        )
        self.conn.commit()

    def get_stats(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT topic, SUM(correct), SUM(total)
        FROM progress
        GROUP BY topic
        """)
        return cursor.fetchall()