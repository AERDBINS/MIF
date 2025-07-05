import sqlite3

conn = sqlite3.connect("tests.db")
cur = conn.cursor()

# Eski jadvalni o‘chirish
cur.execute("DROP TABLE IF EXISTS questions")

# Yangi ustun bilan yaratish
cur.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER,
    question TEXT,
    options TEXT,
    correct_answer TEXT,
    image_path TEXT
)
""")

conn.commit()
conn.close()
print("✅ Jadval yangidan yaratildi")
