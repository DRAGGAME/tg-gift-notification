import asyncio
import logging

from aiogram import Dispatcher

from config import bot
from database.create_table import CreateTable
from handlers.faq_handler import faq_router
from handlers.pay_handler import pay_router
from handlers.start_handler import start_router

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-4s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

dp = Dispatcher()
dp.include_routers(start_router, faq_router, pay_router)


async def main():
    sqlbase_create_table = CreateTable()
    await sqlbase_create_table.connect()
    # await sqlbase_create_table.delete_all()
    await sqlbase_create_table.create_accepted_users_table()
    await sqlbase_create_table.create_settings_table()
    await sqlbase_create_table.create_faq_table()
    await sqlbase_create_table.create_user_table()

    await sqlbase_create_table.close()
    await dp.start_polling(bot)  # Запускаем бота


if __name__ == "__main__":
    asyncio.run(main())
