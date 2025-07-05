from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.constants import MENU_BUTTONS
from bot.keyboards import main_menu_keyboard
from bot.utils.registration_db import update_user_language, load_users
from bot.languages import get_text

router = Router()

# Til tanlash va foydalanuvchiga mos menyu
@router.message(F.text.in_(["🇺🇿 O‘zbek tili", "🇷🇺 Русский язык", "🇬🇧 English"]))
async def set_language(message: Message, state: FSMContext):
    lang_map = {
        "🇺🇿 O‘zbek tili": "uz",
        "🇷🇺 Русский язык": "ru",
        "🇬🇧 English": "en"
    }

    selected_lang = lang_map.get(message.text, "uz")
    user_id = message.from_user.id

    # Foydalanuvchi tilini bazada saqlash (agar foydalanayotgan bo‘lsangiz)
    update_user_language(user_id, selected_lang)

    # FSMda ham saqlab qo‘yamiz
    await state.update_data(lang=selected_lang)

    # Xabar va menyu mos tilga ko‘ra
    welcome_text = get_text("main_menu", selected_lang)
    await message.answer(welcome_text, reply_markup=main_menu_keyboard(selected_lang))


async def get_user_lang(message: Message, state: FSMContext) -> str:
    data = await state.get_data()
    lang = data.get("lang")

    if lang:
        return lang

    # Bazadan olish
    from bot.utils.registration_db import load_users
    user_data = load_users().get(message.from_user.id)

    if user_data:
        return user_data.get("language", "uz")

    return "uz"  # Default
