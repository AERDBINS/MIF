from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from bot.config import CHANNEL_USERNAME


async def check_user_subscription(bot: Bot, user_id: int) -> bool:
    """
    Foydalanuvchining kanalga a'zo ekanligini tekshiradi.

    :param bot: Bot obyekti
    :param user_id: Telegram foydalanuvchi ID
    :return: True agar a'zo bo‘lsa, False aks holda
    """
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except TelegramBadRequest:
        return False
