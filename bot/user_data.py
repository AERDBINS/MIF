# user_data.py
registered_users = {}
user_languages = {}  # Foydalanuvchi tillarini saqlash uchun alohida lug'at

def is_registered(user_id: int) -> bool:
    return user_id in registered_users

def register_user(user_id: int, data: dict):
    registered_users[user_id] = data
    # Ro'yxatdan o'tganda tilni ham saqlash (agar kiritilgan bo'lsa)
    if 'language' in data:
        user_languages[user_id] = data['language']

def get_user_data(user_id: int) -> dict:
    return registered_users.get(user_id, {})

def get_user_language(user_id: int) -> str:
    """Foydalanuvchi tilini olish. Agar yo'q bo'lsa, standart 'uz' qaytaradi"""
    return user_languages.get(user_id, "uz")

def set_user_language(user_id: int, language: str):
    """Foydalanuvchi tilini saqlash"""
    user_languages[user_id] = language
    # Agar foydalanuvchi ro'yxatdan o'tgan bo'lsa, asosiy ma'lumotlarni ham yangilash
    if user_id in registered_users:
        registered_users[user_id]['language'] = language