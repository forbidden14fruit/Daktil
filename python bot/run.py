import asyncio
import logging
import sys
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from aiogram.fsm.storage.memory import MemoryStorage


from app.handlers import router
from config import TOKEN
from config import ADMIN

async def start_bot(bot: Bot):
    await bot.send_message(ADMIN, """Бот запущен

/save - сохранение результатов тестов пользователей
/clear - очистить результаты тестов
/load - загрузить результаты тестов пользователей""")

async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, "Бот остановлен")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    dp.include_routers(router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())