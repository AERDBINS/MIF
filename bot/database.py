import sqlite3
import json

DB_NAME = "tests.db"

# ---------------------------
# 🧱 1. BAZANI YARATISH
# ---------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Testlar jadvali
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        duration_seconds INTEGER NOT NULL
    )
    """)

    # Savollar jadvali (image_path qo‘shildi)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        options TEXT NOT NULL,              -- JSON ko‘rinishida variantlar
        correct_answer TEXT NOT NULL,       -- TO‘G‘RI variant
        image_path TEXT,                    -- 🖼 Rasm fayl yo‘li (ixtiyoriy)
        FOREIGN KEY (test_id) REFERENCES tests (id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

# ---------------------------
# ➕ TEST QO‘SHISH
# ---------------------------
def add_test(title, duration, test_id=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if test_id is None:
        cur.execute("INSERT INTO tests (title, duration_seconds) VALUES (?, ?)", (title, duration))
    else:
        cur.execute("INSERT INTO tests (id, title, duration_seconds) VALUES (?, ?, ?)", (test_id, title, duration))
    conn.commit()
    conn.close()

# ---------------------------
# ➕ SAVOL QO‘SHISH
# ---------------------------
def add_question(test_id, question, options, correct, image_path=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    options_json = json.dumps(options, ensure_ascii=False)
    cur.execute("""
    INSERT INTO questions (test_id, question, options, correct_answer, image_path)
    VALUES (?, ?, ?, ?, ?)
    """, (test_id, question, options_json, correct, image_path))
    conn.commit()
    conn.close()

# ---------------------------
# 🧾 BIR TESTNI OLISH
# ---------------------------
def get_test(test_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, title, duration_seconds FROM tests WHERE id=?", (test_id,))
    row = cur.fetchone()
    conn.close()
    return row

# ---------------------------
# ❓ SAVOLLARNI OLISH
# ---------------------------
def get_questions(test_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, question, options, correct_answer, image_path FROM questions WHERE test_id=?", (test_id,))
    rows = cur.fetchall()
    conn.close()

    result = []
    for q in rows:
        result.append({
            "id": q[0],
            "question": q[1],
            "options": json.loads(q[2]),
            "correct": q[3],
            "image_path": q[4]  # ✅ rasm mavjud bo‘lsa, qaytariladi
        })
    return result

# ---------------------------
# 📋 BARCHA TESTLARNI OLISH
# ---------------------------
def get_all_tests():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM tests ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows
