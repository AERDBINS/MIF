# bot/utils/subscription_middleware.py
from aiogram import BaseMiddleware
from aiogram.types import Update, User, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Callable, Dict, Any, Awaitable
from bot.config import CHANNEL_USERNAME

class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        user: User = data.get("event_from_user")
        bot = data["bot"]

        if not user:
            return await handler(event, data)

        try:
            member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user.id)
            if member.status not in ['member', 'administrator', 'creator']:
                await self.reject(bot, user.id)
                return
        except:
            await self.reject(bot, user.id)
            return

        return await handler(event, data)

    async def reject(self, bot, user_id):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔗 Kanalga a’zo bo‘lish",
                        url=f"https://t.me/{CHANNEL_USERNAME[1:]}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="✅ Tasdiqlash",
                        callback_data="check_subscription"
                    )
                ]
            ]
        )
        await bot.send_message(
            chat_id=user_id,
            text="❌ Iltimos, kanalga a’zo bo‘ling! Aks holda botdan foydalanib bo‘lmaydi.",
            reply_markup=keyboard
        )
