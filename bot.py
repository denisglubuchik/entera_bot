import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config


async def main():
    config: Config = load_config()

    # engine = create_async_engine(url=config.db.db_url)
    # sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=config.tgbot.token,
              parse_mode='HTML')

    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())