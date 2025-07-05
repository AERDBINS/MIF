from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from bot.config import CHANNEL_USERNAME

router = Router()

@router.callback_query(F.data == "check_subscription")
async def check_subscription(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    bot = call.bot

    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            await call.message.delete()

            # Holatni tekshiramiz (avvalgi amaliyot bor yoki yo'q)
            current_state = await state.get_state()
            if current_state and current_state != default_state:
                # Avvalgi amaliyot mavjud => davom etishiga ruxsat
                await call.answer("✅ Tekshirildi. Davom ettiring.")
            else:
                # Hech qanday amaliyot yo‘q => menyuni ko‘rsatamiz
                menu_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="🧪 Test ishlash", callback_data="start_test")],
                        [InlineKeyboardButton(text="📚 Kitoblar", callback_data="show_books")]
                    ]
                )
                await bot.send_message(
                    chat_id=user_id,
                    text="Botdan foydalanish uchun menyudan tanlang:",
                    reply_markup=menu_keyboard
                )
        else:
            await call.answer("❌ Siz hali kanalga a’zo emassiz.", show_alert=True)
    except:
        await call.answer("⚠️ Xatolik. Keyinroq urinib ko‘ring.", show_alert=True)