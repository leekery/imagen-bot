from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, Router, F
from config.whitelist_loader import whitelist
from loader import TOKEN

import asyncio
import logging

from handlers.start import router as start_router

router = Router()

async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    bot = Bot(
        TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    logger.info("Бот успешно запущен")
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(start_router)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())