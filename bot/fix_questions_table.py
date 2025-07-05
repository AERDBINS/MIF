import sqlite3

conn = sqlite3.connect("tests.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS questions")

cur.execute("""
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER,
    question TEXT,
    options TEXT,
    correct TEXT
)
""")

conn.commit()
conn.close()
print("✅ 'questions' jadvali to‘g‘ri yaratildi.")
import sqlite3

conn = sqlite3.connect("tests.db")
cur = conn.cursor()
cur.execute("PRAGMA table_info(questions)")
print(cur.fetchall())
