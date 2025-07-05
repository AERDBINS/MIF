# bot/utils_common.py
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.utils.registration_db import load_users

async def get_user_lang(message: Message, state: FSMContext) -> str:
    """
    Foydalanuvchi tanlagan tilni qaytaradi.
    Avval FSM state dan tekshiradi,
    bo‘lmasa bazadan izlaydi.
    """

    # FSMState dan tekshir
    data = await state.get_data()
    lang = data.get("lang")
    if lang:
        return lang

    # Bazadan tekshir
    user_data = load_users().get(message.from_user.id)
    if user_data:
        return user_data.get("language", "uz")

    # Hech qayerdan topilmasa, default o‘zbekcha
    return "uz"
