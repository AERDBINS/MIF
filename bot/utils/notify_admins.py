# bot/utils/notify_admins.py

from aiogram import Bot
from bot.config import ADMIN_IDS

async def send_to_admins(bot: Bot, text: str):
    for admin_id in ADMIN_IDS:
        await bot.send_message(chat_id=admin_id, text=text, parse_mode="HTML")
