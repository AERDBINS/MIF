import sqlite3
import json

conn = sqlite3.connect("tests.db")
cur = conn.cursor()

print("🔎 TESTLAR:")
cur.execute("SELECT id, title FROM tests")
tests = cur.fetchall()
for t in tests:
    print(t)

print("\n🧪 SAVOLLAR:")
cur.execute("SELECT test_id, question FROM questions")
questions = cur.fetchall()
for q in questions:
    print(f"TestID: {q[0]} | Savol: {q[1]}")
