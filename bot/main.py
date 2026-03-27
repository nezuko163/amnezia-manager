import asyncio, os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from bot.handlers import main_menu, clients, server

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID"))

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Middleware для проверки доступа
    @dp.message.middleware()
    @dp.callback_query.middleware()
    async def auth_middleware(handler, event, data):
        user_id = event.from_user.id
        if user_id != ALLOWED_USER_ID:
            return
        return await handler(event, data)

    dp.include_router(main_menu.router)
    dp.include_router(clients.router)
    dp.include_router(server.router)

    print("🤖 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
