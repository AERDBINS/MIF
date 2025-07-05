from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.keyboards import main_menu_keyboard, subscribe_keyboard, language_keyboard
from bot.utils.check_subscription import check_user_subscription

router = Router()

lang_map = {
    "🇺🇿 O‘zbek tili": "uz",
    "🇷🇺 Русский язык": "ru",
    "🇬🇧 English": "en"
}

@router.message(F.text == "/start")
async def start_handler(message: Message, bot, state: FSMContext):
    user_id = message.from_user.id
    is_member = await check_user_subscription(bot, user_id)

    if not is_member:
        await message.answer("⚠️ Iltimos, kanalga a’zo bo‘ling:", reply_markup=subscribe_keyboard())
        return

    await state.clear()  # eski holatni tozalash
    await message.answer("🇺🇿 Iltimos, tilni tanlang:", reply_markup=language_keyboard())


@router.message(F.text.in_(lang_map.keys()))
async def set_language(message: Message, state: FSMContext):
    lang = lang_map.get(message.text, "uz")
    await state.update_data(lang=lang)

    await message.answer("🏠 Asosiy menyu:", reply_markup=main_menu_keyboard(lang))


@router.callback_query(F.data == "check_subscription")
async def check_sub(call: CallbackQuery, bot, state: FSMContext):
    user_id = call.from_user.id
    if await check_user_subscription(bot, user_id):
        await call.message.delete()
        current_state = await state.get_state()

        if current_state and current_state != default_state:
            await call.answer("✅ Obuna tasdiqlandi. Davom eting.")
            # foydalanuvchi ayni vaqtda qayerda bo‘lsa, o‘sha joyda qoladi
        else:
            # Hech qanday holat bo‘lmasa — menyu yoki til tanlashga yuboriladi
            data = await state.get_data()
            lang = data.get("lang", "uz")
            if lang in lang_map.values():
                await call.message.answer("🏠 Asosiy menyu:", reply_markup=main_menu_keyboard(lang))
            else:
                await call.message.answer("🇺🇿 Iltimos, tilni tanlang:", reply_markup=language_keyboard())
    else:
        await call.answer("🚫 Siz hali kanalga obuna bo‘lmagansiz!", show_alert=True)
