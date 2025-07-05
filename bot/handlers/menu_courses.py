from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from pathlib import Path
import json

from bot.languages import get_text
from bot.keyboards import main_menu_keyboard
from bot.utils.registration_db import is_registered, load_users
from bot.states.registration import Registration
from bot.config import ADMIN_IDS
from bot.utils.notify_admins import send_to_admins

router = Router()

# Kurslar va ma’lumotlari
courses = [
    "📊 Matematika",
    "🔭 Fizika",
    "🇬🇧 Ingliz tili",
    "📜 Tarix",
    "📚 Ona tili va adabiyot",
    "🚗 Haydovchilik testi"
]

course_texts = {
     "📊 Matematika": (
        "<b>📊 Matematika kursi</b>\n\n"
        "🧑🏻‍🏫 <b>Ustoz:</b> Sobir Sayitov (12+ yillik tajriba)\n"
        "🎓 O‘quvchilari OTMlarda – 2000+\n"
        "🌟 Darajasi: A+\n\n"
        "📘 <b>Nimalar o‘rganiladi:</b>\n"
        "– Algebra, geometriya, matematik tahlil\n"
        "– Test tahlili va yechim strategiyalari\n\n"
        "📆 <b>Kurs davomiyligi:</b> Haftada 3 kun\n"
        "💵 <b>To‘lov:</b> Dars shakliga qarab\n"
        "🌐 <b>Dars shakli:</b> Online, Offline va Individual\n\n"
        "☎️ <b>Aloqa:</b> +998 90 348 24 48\n"
        "📲 <b>Telegram:</b> @Sobir_Sayitov"
    ),
    "🔭 Fizika": (
        "<b>🔭 Fizika kursi</b>\n\n"
        "👩‍🏫 <b>Ustoz:</b> Jo'rayeva Shahnoza (11+ yillik tajriba)\n"
        "🎓 O‘quvchilari OTMlarda – 2000+\n"
        "✅ <b>Kurs mazmuni:</b>\n"
        "• Fizika asosiy tushunchalari va nazariy bilimlarni o‘rgatish\n"
        "• Maktab va abituriyent test savollariga tayyorlash\n"
        "• Masala yechish usullari va test strategiyalarini tushuntirish\n\n"
        "📆 <b>Kurs davomiyligi:</b> Haftada 3 kun\n"
        "💵 <b>To‘lov:</b> Oyiga 400 000 so‘m \n"
        "🌐 <b>Dars shakli:</b> Online va Offline\n\n"
        "☎️ <b>Aloqa:</b> +998 90 348 24 48\n"
        "📲 <b>Telegram:</b> @Sobir_Sayitov"

    ),
    "🇬🇧 Ingliz tili": (
        "<b>🇬🇧 Ma'lumot olish uchun biz bog'laning</b>\n"
        "☎️ <b>Aloqa:</b> +998 90 348 24 48\n"
        "📲 <b>Telegram:</b> @Sobir_Sayitov"

    ),

    "📜 Tarix": (
        "<b>📜 Tarix kursi</b>\n\n"
        "🧑‍🏫 <b>Ustoz:</b> Muhammadyusuf Mo'ydinov (7+ yillik tajriba)\n"
        "🎓 O‘quvchilari OTMlarda – 500+\n"
        "✅ <b>Kurs mazmuni:</b>\n"
        "• Tarix asosiy tushunchalari va nazariy bilimlarni o‘rgatish\n"
        "• Maktab va abituriyent test savollariga tayyorlash\n"
        "• Tarixiy voqealarni tahlil qilish va yodlash usullarini tushuntirish\n\n"
        "📆 <b>Kurs davomiyligi:</b> Haftada 3 kun\n"
        "💵 <b>To‘lov:</b> Oyiga 400 000 so‘m \n"
        "🌐 <b>Dars shakli:</b> Online va Offline\n\n"
        "☎️ <b>Aloqa:</b> +998 90 348 24 48 \n"
        "📲 <b>Telegram:</b> @Sobir_Sayitov\n"
    ),
    "📚 Ona tili va adabiyot": (
        "<b>📚 Ona tili va adabiyot kursi</b>\n\n"
        "🧑‍🏫 <b>Ustoz:</b> Muhammadyusuf Mo'ydinov (5+ yillik tajriba)\n"
        "🎓 O‘quvchilari OTMlarda – 500+\n"
        "✅ <b>Kurs mazmuni:</b>\n"
        "• Ona tili grammatikasi va asosiy qo‘idalarini o‘rgatish\n"
        "• Adabiyotdan nazariy bilimlar va tahlil qilish ko‘nikmalarini rivojlantirish\n"
        "• Maktab va abituriyent test savollariga tayyorlash\n"
        "• Matnlarni tahlil qilish va savol-javob usullari bilan ishlash\n\n"
        "📆 <b>Kurs davomiyligi:</b> Haftada 3 kun\n"
        "💵 <b>To‘lov:</b> Oyiga 400 000 so‘m \n"
        "🌐 <b>Dars shakli:</b> Online va Offline\n\n"
        "☎️ <b>Aloqa:</b> +998 90 348 24 48 \n"
        "📲 <b>Telegram:</b> @Sobir_Sayitov\n"
    ),
    "🚗 Haydovchilik testi": (
        "🚗 Haydovchilik kursi: YHQ, Nazariy testlar(1130 ta savol).\n\n"
        "🧑🏿‍🏫 <b>Ustoz:</b> Igamberdiyev Otabek (2+ yillik tajriba)\n"
        "🎓 Doimiy 100% lik natijalar\n\n"
        "✅ <b>Kurs mazmuni:</b>\n"
        "• Yo‘l harakati qoidalari (YHQ) bo‘yicha nazariy bilimlarni o‘rgatish\n"
        "• Test savollariga tayyorlash\n"
        "• Nazariy mashg‘ulotlar orqali test yechish usullarini tushuntirish\n"
        "• Nazariy test sinovlaridan 1 urunishda o'tish\n\n"
        "📆 <b>Kurs davomiyligi:</b> 10 kun+\n"
        "⏰ <b>Dars vaqti:</b> Har kuni 2 soatdan (Yakshanba dam) \n\n"
        "🌐 <b>Dars shakli:</b> Offline\n"
        "☎️ <b>Aloqa:</b> +998 90 348 24 48 \n"
        "📲 <b>Telegram:</b> @Sobir_Sayitov\n"
    )
}

@router.message(F.text.in_ (["📚 Kurslar","📚 Courses","📚 Курсы"])  )
async def show_courses_menu(message: Message):
    lang = "uz"

    keyboard = []
    for i in range(0, len(courses), 2):
        row = [KeyboardButton(text=courses[i])]
        if i + 1 < len(courses):
            row.append(KeyboardButton(text=courses[i + 1]))
        keyboard.append(row)

    keyboard.append([KeyboardButton(text="🏠 Asosiy menyu")])

    # Fallback bilan placeholder
    placeholder = get_text("Kursni tanlang", lang) or "📚 Kursni tanlang"

    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )

    await message.answer(placeholder, reply_markup=markup)

@router.message(F.text == "🏠 Asosiy menyu")
async def back_to_main_menu(message: Message):
    lang = "uz"
    await message.answer(get_text("main_menu", lang), reply_markup=main_menu_keyboard(lang))

@router.message(F.text.in_(courses))
async def course_info(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✍️ Kursga yozilish")],
            [KeyboardButton(text="🔙 Ortga")]
        ],
        resize_keyboard=True
    )
    await message.answer(course_texts.get(message.text, "№ Ma'lumot topilmadi."), reply_markup=keyboard)

@router.message(F.text == "✍️ Kursga yozilish")
async def enroll_course(message: Message, state: FSMContext):
    user_id = message.from_user.id
    users = load_users()
    user_data = next((user for user in users if user["id"] == user_id), None)

    if user_data:
        data = await state.get_data()
        course = data.get("course", "Noma’lum kurs")

        msg = f"""\
📅 <b>Yangi kursga yozilish:</b>
👤 Ism: <b>{user_data['name']}</b>
📞 Tel: <b>{user_data['phone']}</b>
📚 Kurs: <b>{course}</b>
🔗 Telegram: <a href="tg://user?id={user_id}">{user_id}</a>

✅ /confirm_{user_id}_{course.replace(' ', '_')}
❌ Bekor qilish: /cancel_{user_id}_{course.replace(' ', '_')}
"""
        await send_to_admins(message.bot, msg)
        await message.answer("✅ Arizangiz yuborildi! Tez orada siz bilan bog‘lanamiz.", reply_markup=main_menu_keyboard("uz"))
    else:
        # ⬇️ Inline tugmalar bilan ro‘yxatdan o‘tishga yo‘naltiramiz
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 Ro‘yxatdan o‘tish", callback_data="start_register")],
            [InlineKeyboardButton(text="🔙 Ortga", callback_data="back_to_courses")]
        ])

        await message.answer(
            "❗️Siz hali ro‘yxatdan o‘tmagansiz. Iltimos, avval ro‘yxatdan o‘ting.",
            reply_markup=markup
        )
@router.message(F.text == "🔙 Ortga")
async def back_to_courses(message: Message):
    await show_courses_menu(message)

ENROLLMENT_FILE = Path("data/enrollments.json")

def save_enrollments(data):
    ENROLLMENT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ENROLLMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_enrollments():
    if ENROLLMENT_FILE.exists():
        with open(ENROLLMENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# ✅ Kursni tasdiqlash — /confirm_<id>_<kurs_nomi>
@router.message(F.text.startswith("/confirm_"))
async def confirm_course(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    try:
        _, user_id_str, *kurs_parts = message.text.split("_")
        user_id = int(user_id_str)
        course = " ".join(kurs_parts)
    except Exception:
        await message.answer("❌ Format xato. To‘g‘ri format: /confirm_<id>_<kurs>")
        return

    enrollments = load_enrollments()
    if any(e["id"] == user_id and e["course"] == course for e in enrollments):
        await message.answer("⚠️ Bu foydalanuvchi allaqachon ushbu kursga tasdiqlangan.")
        return

    users = load_users()
    user_data = next((u for u in users if u["id"] == user_id), {})

    enrollments.append({
        "id": user_id,
        "course": course,
        "name": user_data.get("name", "Noma'lum"),
        "phone": user_data.get("phone", "—"),
        "paid": False
    })

    save_enrollments(enrollments)

    await message.bot.send_message(
        user_id,
        f"✅ Siz <b>{course}</b> kursiga muvaffaqiyatli yozildingiz!",
        parse_mode="HTML"
    )
    await message.answer("☑️ Foydalanuvchi tasdiqlandi.")

# ✅ Kursni bekor qilish — /cancel_<id>_<kurs_nomi>
@router.message(F.text.startswith("/cancel_"))
async def cancel_course(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    try:
        _, user_id_str, *kurs_parts = message.text.split("_")
        user_id = int(user_id_str)
        course = " ".join(kurs_parts)
    except Exception:
        await message.answer("❌ Format xato. To‘g‘ri format: /cancel_<id>_<kurs>")
        return

    enrollments = load_enrollments()
    if not any(e["id"] == user_id and e["course"] == course for e in enrollments):
        await message.answer("⚠️ Bu foydalanuvchi bu kursga yozilmagan.")
        return

    new_enrollments = [
        e for e in enrollments if not (e["id"] == user_id and e["course"] == course)
    ]
    save_enrollments(new_enrollments)

    await message.bot.send_message(
        user_id,
        f"❌ Siz <b>{course}</b> kursidan chiqarildingiz.",
        parse_mode="HTML"
    )
    await message.answer("🚫 Kurs bekor qilindi.")

# ✅ To‘lovni belgilash — /pay_<id>_<kurs_nomi>
@router.message(F.text.startswith("/pay_"))
async def mark_as_paid(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    try:
        _, user_id_str, *kurs_parts = message.text.split("_")
        user_id = int(user_id_str)
        course = " ".join(kurs_parts)
    except Exception:
        await message.answer("❌ Format xato. To‘g‘ri format: /pay_<id>_<kurs>")
        return

    enrollments = load_enrollments()
    updated = False
    for e in enrollments:
        if e["id"] == user_id and e["course"] == course:  # 🛠 faqat shu kurs uchun
            e["paid"] = True
            updated = True
            break

    if updated:
        save_enrollments(enrollments)
        await message.answer(f"✅ <b>{course}</b> bo‘yicha to‘lov holati yangilandi.", parse_mode="HTML")
    else:
        await message.answer("❗️ Foydalanuvchi yoki kurs topilmadi.")

@router.message(F.text == "Statistika")
async def show_statistics(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("❌ Sizga bu buyruq ruxsat etilmagan.")

    enrollments = load_enrollments()
    if not enrollments:
        return await message.answer("📭 Hali hech kim kursga yozilmagan.")

    stat_msg = "📊 <b>Kurslar bo‘yicha statistika:</b>\n\n"
    course_summary = {}

    for item in enrollments:
        course = item["course"]
        if course not in course_summary:
            course_summary[course] = {
                "total": 0,
                "paid": 0,
                "students": []
            }

        course_summary[course]["total"] += 1
        if item.get("paid"):
            course_summary[course]["paid"] += 1

        course_summary[course]["students"].append(item)

    for course, data in course_summary.items():
        stat_msg += f"📘 <b>{course}</b>\n"
        stat_msg += f"👥 Jami: <b>{data['total']}</b> | 💳 To‘laganlar: <b>{data['paid']}</b>\n"

        for s in data["students"]:
            status = "✅" if s.get("paid") else "❌"
            stat_msg += f"— {s['name']} | {s['phone']} | {status}\n"

        stat_msg += "\n"

    await message.answer(stat_msg, parse_mode="HTML")


