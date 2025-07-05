from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.handlers.registration import start_registration  # MUHIM! to‘g‘ri yo‘l bo‘lsin

router = Router()

@router.callback_query(F.data == "start_register")
async def handle_register_callback(callback: CallbackQuery, state: FSMContext):
    # Inline tugma bosilganda ro‘yxatdan o‘tish funksiyasiga yo‘naltirish
    await start_registration(callback.message, state)
    await callback.answer()
