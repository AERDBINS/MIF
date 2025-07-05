import sqlite3

conn = sqlite3.connect("tests.db")
cur = conn.cursor()

cur.execute("SELECT id, question, image_path FROM questions WHERE image_path IS NOT NULL")
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
