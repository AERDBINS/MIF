import json
from pathlib import Path

USERS_FILE = Path("data/users.json")
def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_users(user_data: dict):
    users = load_users()

    # Agar foydalanuvchi allaqachon mavjud bo‘lsa, yangilamasin
    if any(u["id"] == user_data["id"] for u in users):
        return

    users.append(user_data)

    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def update_user_language(user_id: int, lang: str):
    users = load_users()
    for user in users:
        if user["id"] == user_id:
            user["lang"] = lang
            break
    else:
        users.append({"id": user_id, "lang": lang})
    save_users(users)

def get_user_language(user_id: int) -> str:
    users = load_users()
    for user in users:
        if user["id"] == user_id:
            return user.get("lang", "uz")
    return "uz"

def is_registered(user_id: int) -> bool:
    users = load_users()
    return any(u["id"] == user_id for u in users)

