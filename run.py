import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import PreCheckoutQuery
from apscheduler.triggers.interval import IntervalTrigger

from config import bot
from database.admin_operations import AdminOperations
from database.create_table import CreateTable
from handlers.admin_handlers.main_handlers import router_for_main
from handlers.user_handlers import router_for_admin
from handlers.stop_handler import router_for_stop

from schedulers.scheduler_object import scheduler
from schedulers.starts import start_cmd

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-4s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

dp = Dispatcher()
dp.include_routers(router_for_admin, router_for_stop, router_for_main)

@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


async def main():
    sqlbase_create_table = CreateTable()
    await sqlbase_create_table.connect()
    # await sqlbase_create_table.delete_all()
    await sqlbase_create_table.create_profiles_table()
    await sqlbase_create_table.create_settings_table()
    await sqlbase_create_table.create_transaction_donat()
    sqlbase_admin = AdminOperations()
    scheduler.add_job(start_cmd, IntervalTrigger(minutes=1), args=[sqlbase_admin])
    scheduler.start()
    await dp.start_polling(bot)  # Запускаем бота


if __name__ == "__main__":
    asyncio.run(main())
