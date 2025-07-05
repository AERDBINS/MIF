from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from bot.keyboards import main_menu_keyboard, language_keyboard
from bot.utils.registration_db import load_users

router = Router()

# Sozlamalar menyusi
@router.message(F.text.in_(["⚙️ Sozlamalar", "⚙️ Настройки", "⚙️ Settings"]))
async def show_settings_menu(message: Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌐 Tilni o‘zgartirish")],
            [KeyboardButton(text="📘 Mening kurslarim")],
            [KeyboardButton(text="📝 Profilim")],
            [KeyboardButton(text="🏠 Asosiy menyu")]
        ],
        resize_keyboard=True
    )
    await message.answer("⚙️ Sozlamalar menyusiga xush kelibsiz!", reply_markup=markup)

# 1. Tilni o‘zgartirish
@router.message(F.text == "🌐 Tilni o‘zgartirish")
async def change_language(message: Message):
    await message.answer("Iltimos, tilni tanlang:", reply_markup=language_keyboard())

# 4. Mening kurslarim (data/enrollments.json asosida)
import json
from pathlib import Path

ENROLLMENT_FILE = Path("data/enrollments.json")

def load_enrollments():
    if ENROLLMENT_FILE.exists():
        with open(ENROLLMENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.message(F.text == "📘 Mening kurslarim")
async def my_courses(message: Message):
    user_id = message.from_user.id
    enrollments = load_enrollments()
    user_courses = [e["course"] for e in enrollments if e["id"] == user_id]

    if not user_courses:
        await message.answer("📭 Siz hech qanday kursga yozilmagansiz.")
    else:
        text = "📘 Siz yozilgan kurslar:\n" + "\n".join(f"✅ {c}" for c in user_courses)
        await message.answer(text)

@router.message(F.text == "📝 Profilim")
async def show_profile(message: Message):
    users = load_users()
    user_data = next((u for u in users if u["id"] == message.from_user.id), None)

    if user_data:
        msg = (
            f"👤 <b>Ism:</b> {user_data['name']}\n"
            f"📞 <b>Telefon:</b> {user_data['phone']}\n"
            f"🆔 <b>ID:</b> <code>{message.from_user.id}</code>"
        )
    else:
        msg = "❗️ Siz hali ro‘yxatdan o‘tmagansiz."

    await message.answer(msg, parse_mode="HTML")
