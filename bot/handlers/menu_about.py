from aiogram import Router, F
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery
)
from aiogram.types.input_file import FSInputFile
from bot.languages import get_text
import os

router = Router()

# 🎓 O‘quv markazi haqida matn
about_text = (
    "🏫 <b>MIF School</b>\n\n"
    "📍 <b>Manzil:</b> <a href='https://maps.app.goo.gl/8H4CBBGVBi2szByB9'>Xaritada ko‘rish</a>\n"
    "📞 <b>Telefon:</b> +998903482448\n\n"
    "🕒 <b>Ish vaqti:</b>\n"
    "Dushanba–Shanba: 08:00 – 22:00\n"
    "Yakshanba: dam olish kuni\n\n"
    "👨‍🏫 <b>Ustozlar:</b>\n"
    "Har bir yo‘nalishda tajribali ustozlar!\n"
    "Ustozlarni natijalarini pastagi tugmlar orqali ko'rishingiz  mumkin.\n\n"
    "🌐 <b>Dars shakli:</b>\n"
    "Online va Offline darslar"
)

# 🌐 Ijtimoiy tarmoqlar tugmalari
about_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📢 Telegram", url="https://t.me/MIF_School")],
    [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/mif_school")],
    [InlineKeyboardButton(text="▶️ YouTube", url="https://youtube.com/@Sayitov_Sobir")],
    [InlineKeyboardButton(text="👨‍🏫 O‘qituvchilar haqida", callback_data="about_teachers")]
])

# 🧑‍🏫 O‘qituvchilar ro‘yxati: Ism -> rasm yo‘li
teachers = {
    "Sobir Sayitov": "image/Sobir_Sayitov.png",
    "Jo'rayeva Shahnoza": "image/Jo'rayeva_Shahnoza.png",
    "Muhammadyusuf Mo'ydinov": "image/Muhammadyusuf.png",
    "Igamberdiyev Otabek": "image/Igamberdiyev_Otabek.png"
}

# 🎓 O‘quv markazi haqida tugmasi bosilganda
@router.message(F.text.in_ ([ "🎓 O‘quv markazi haqida","🎓 О учебном центре","🎓 About the Center"]))
async def about_handler(message: Message):
    await message.answer(about_text, reply_markup=about_buttons, parse_mode="HTML", disable_web_page_preview=True)

# 👨‍🏫 O‘qituvchilar haqida tugmasi bosilganda
@router.callback_query(F.data == "about_teachers")
async def teachers_info(callback: CallbackQuery):
    # O‘qituvchilar ro‘yxati tugmalari
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=name, callback_data=f"teacher_{name}")]
        for name in teachers
    ])
    await callback.message.answer("Quyidagi ustozlardan birini tanlang:", reply_markup=keyboard)
    await callback.answer()

# 🖼 Har bir ustozni bosganda — rasmi yuboriladi
@router.callback_query(F.data.startswith("teacher_"))
async def show_teacher_photo(callback: CallbackQuery):
    teacher_name = callback.data.replace("teacher_", "")
    photo_path = teachers.get(teacher_name)

    if photo_path and os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await callback.message.answer_photo(photo, caption=f"👤 {teacher_name}")
    else:
        await callback.message.answer("❌ Rasm topilmadi.")
    await callback.answer()
