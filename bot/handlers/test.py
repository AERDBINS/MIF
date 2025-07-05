from aiogram import Router, F, Bot
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.keyboards import main_menu_keyboard
from bot.database import get_test, get_questions
from bot.config import ADMIN_IDS, BOT_TOKEN
from .inline_test_buttons import generate_test_buttons
import random, asyncio
import html
from aiogram.types.input_file import FSInputFile

router = Router()

# 📋 Test menyusi
@router.message(F.text.in_(["🧪 Test", "🧪 Тест", "🧪 Test"]))
async def show_test_menu(message: Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧮 Matematika testi"), KeyboardButton(text="🌍 Tarix testi")],
            [KeyboardButton(text="✏️ Ona tili va adabiyot"), KeyboardButton(text="🗣 Ingliz tili")],
            [KeyboardButton(text="🛞 Haydovchilik testi")],
            [KeyboardButton(text="↩️ Ortga")]
        ],
        resize_keyboard=True
    )
    await message.answer("Quyidagi testlardan birini tanlang:", reply_markup=markup)

# 🧮 Maxsus matematika testi
@router.message(F.text == "🧮 Matematika testi")
async def show_math_test_button(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="▶️ 30 ta testni boshlash",
        callback_data="start_test_1"  # test_id mos ravishda bo‘lishi kerak
    ))
    await message.answer(
        "🧮 Siz Matematika testini boshlamoqchisiz. Quyidagi tugmani bosing:",
        reply_markup=builder.as_markup()
    )
@router.message(F.text == "🌍 Tarix testi")
async def show_history_test_button(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="▶️ 30 ta testni boshlash",
        callback_data="start_test_2"  # test_id = 2
    ))
    await message.answer("🌍 Tarix testi. Boshlash uchun pastdagi tugmani bosing:", reply_markup=builder.as_markup())

@router.message(F.text == "✏️ Ona tili va adabiyot")
async def show_literature_test_button(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="▶️ 30 ta testni boshlash",
        callback_data="start_test_3"  # test_id = 3
    ))
    await message.answer("✏️ Ona tili testi. Boshlash uchun pastdagi tugmani bosing:", reply_markup=builder.as_markup())

@router.message(F.text == "🗣 Ingliz tili")
async def show_english_test_button(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="▶️ 30 ta testni boshlash",
        callback_data="start_test_4"  # test_id = 4
    ))
    await message.answer("🗣 Ingliz tili testi. Boshlash uchun pastdagi tugmani bosing:", reply_markup=builder.as_markup())

@router.message(F.text == "🛞 Haydovchilik testi")
async def show_driving_test_button(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="▶️ 30 ta testni boshlash",
        callback_data="start_test_5"  # test_id = 5
    ))
    await message.answer("🛞 Haydovchilik testi. Boshlash uchun pastdagi tugmani bosing:", reply_markup=builder.as_markup())
# 📚 Barcha testlar ro‘yxati
@router.message(F.text == "🧪 Testlar ro‘yxati")
async def show_all_tests(message: Message):
    keyboard = generate_test_buttons()
    await message.answer("📚 Mavjud testlar ro‘yxati:", reply_markup=keyboard)

# ▶️ Testni boshlash
@router.callback_query(F.data.startswith("start_test_"))
async def start_test_from_inline(callback: CallbackQuery, state: FSMContext):
    try:
        test_id = int(callback.data.split("_")[-1])
        test = get_test(test_id)
        questions = get_questions(test_id)

        if not test or not questions:
            return await callback.message.answer("❌ Test topilmadi yoki savollar mavjud emas")

        random.shuffle(questions)

        await state.set_data({
            "questions": questions,
            "index": 0,
            "correct": 0,
            "correct_ids": [],
            "total": len(questions),
            "test_id": test_id
        })

        asyncio.create_task(end_test_after_timeout(callback.message.chat.id, test[2], state))
        await callback.message.answer("✅ Test boshlandi!")
        await send_question(callback.message, questions[0])

    except Exception as e:
        print("❌ Xatolik:", e)
        await callback.message.answer("⚠️ Testni boshlashda xatolik yuz berdi.")

# ❓ Savol yuborish
async def send_question(msg, question):
    import html
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=v, callback_data=f"answer_{question['id']}_{v}")]
            for v in question['options']
        ]
    )

    safe_question = html.escape(question['question'])

    if question.get("image_path"):
        try:
            photo = FSInputFile(question["image_path"])  # ✅ image/q29.png
            await msg.answer_photo(
                photo=photo,
                caption=f"❓ {safe_question}",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"❌ Rasm yuklash xatoligi: {e}")
            await msg.answer(f"❓ {safe_question}\n(Rasm yuklanmadi)", reply_markup=keyboard, parse_mode="HTML")
    else:
        await msg.answer(f"❓ {safe_question}", reply_markup=keyboard, parse_mode="HTML")
# /start_quiz <id>
@router.message(F.text.startswith("/start_quiz"))
async def start_quiz_command(message: Message, state: FSMContext):
    try:
        _, test_id = message.text.split()
        test_id = int(test_id)
        test = get_test(test_id)
        questions = get_questions(test_id)

        if not test or not questions:
            return await message.answer("❌ Test topilmadi yoki savollar mavjud emas.")

        random.shuffle(questions)
        await state.set_data({
            "questions": questions,
            "index": 0,
            "correct": 0,
            "correct_ids": [],
            "total": len(questions),
            "test_id": test_id
        })

        asyncio.create_task(end_test_after_timeout(message.chat.id, test[2], state))
        await message.answer("✅ Test boshlandi!")
        await send_question(message, questions[0])

    except Exception as e:
        print("❌ /start_quiz xatolik:", e)
        await message.answer("⚠️ Format noto‘g‘ri. To‘g‘ri format: /start_quiz <test_id>")

# ✅ Javobni tekshirish
@router.callback_query(F.data.startswith("answer_"))
async def handle_quiz_answer(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_", 2)
    savol_id = int(parts[1])
    user_answer = parts[2]

    data = await state.get_data()
    if not data:
        return await callback.answer("⏰ Test vaqti tugagan!", show_alert=True)

    index = data['index']
    correct = data['correct']
    questions = data['questions']
    correct_ids = data.get("correct_ids", [])

    current = questions[index]
    if savol_id != current['id']:
        return await callback.answer("⛔ Bu savolga allaqachon javob berilgan")

    if user_answer == current['correct']:
        correct += 1
        correct_ids.append(str(index + 1))

    index += 1

    if index >= len(questions):
        await state.clear()
        result_text = (
            f"✅ Test yakunlandi!\n"
            f"Natija: {correct}/{len(questions)}\n"
            f"To‘g‘ri javoblar: {', '.join(correct_ids) if correct_ids else 'Hech biri'}"
        )
        await callback.message.answer(result_text)
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(
            ADMIN_IDS,
            f"📊 @{callback.from_user.username or callback.from_user.full_name} natijasi: {correct}/{len(questions)}"
        )
        return

    await state.update_data(index=index, correct=correct, correct_ids=correct_ids)
    await send_question(callback.message, questions[index])

# ⏰ Vaqt tugashi
async def end_test_after_timeout(chat_id, seconds, state: FSMContext):
    await asyncio.sleep(seconds)
    data = await state.get_data()
    if data:
        correct = data.get("correct", 0)
        total = data.get("total", 0)
        await state.clear()
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id, f"⏰ Test vaqti tugadi!\nTo‘g‘ri javoblar: {correct}/{total}")
        await bot.send_message(ADMIN_IDS, f"📊 Test Vaqti Tugadi - Natija: {correct}/{total} - Chat ID: {chat_id}")

# 🔙 Ortga
@router.message(F.text == "↩️ Ortga")
async def back_to_main_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    await message.answer("🏠 Asosiy menyu", reply_markup=main_menu_keyboard(lang))
