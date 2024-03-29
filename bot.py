import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import config
from handlers import handlers, template_handlers, broadcast_message_handlers
from keyboards import set_main_menu

logger = logging.getLogger(__name__)
# config: Config = load_config()


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
    dp.include_router(template_handlers.router)
    dp.include_router(broadcast_message_handlers.router)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    print()

if __name__ == '__main__':
    asyncio.run(main())
