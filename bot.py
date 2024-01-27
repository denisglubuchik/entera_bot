import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from handlers import handlers
from keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)
config: Config = load_config()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    bot = Bot(token=config.tgbot.token)

    dp = Dispatcher()
    dp.include_router(handlers.router)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
