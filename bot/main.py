import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers import routers
from set_commands import set_admin_commands
from bot.database import init_db
from utils.subscription_middleware import SubscriptionMiddleware  # ✅ YANGI

async def main():
    print("✅ Bot ishga tushmoqda...")

    init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # ✅ Kanalga a’zo bo‘lishni har bir handlerdan oldin tekshirish

    dp.message.middleware(SubscriptionMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())
    for router in routers:
        dp.include_router(router)

    await set_admin_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
