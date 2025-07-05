import sqlite3
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_test_buttons():
    conn = sqlite3.connect("../tests.db")
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM tests")
    rows = cur.fetchall()
    conn.close()

    keyboard = InlineKeyboardMarkup(row_width=1)

    for row in rows:
        test_id, title = row
        button = InlineKeyboardButton(
            text=f"📘 {title}",
            callback_data=f"start_test_{test_id}"
        )
        keyboard.add(button)

    return keyboard
