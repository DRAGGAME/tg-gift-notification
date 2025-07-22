import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import PreCheckoutQuery
from apscheduler.triggers.interval import IntervalTrigger

from config import bot
from database.create_table import CreateTable
from handlers.admin_handlers.all_a_admin_function import router_for_admin
from handlers.admin_handlers.update_url import url_router
from handlers.stop_handler import router_for_stop
from handlers.user_handlers.donate_handler import donate_router
from handlers.user_handlers.faq_handler import faq_router
from handlers.user_handlers.pay_handler import pay_router
from handlers.user_handlers.start_handler import start_router
from schedulers.scheduler_object import scheduler
from schedulers.starts import start_cmd

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-4s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

dp = Dispatcher()
dp.include_routers(start_router, faq_router, pay_router, router_for_admin, url_router, donate_router, router_for_stop)

@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


async def main():
    sqlbase_create_table = CreateTable()
    await sqlbase_create_table.connect()
    # await sqlbase_create_table.delete_all()
    await sqlbase_create_table.create_accepted_users_table()
    await sqlbase_create_table.create_settings_table()
    await sqlbase_create_table.create_transaction_donat()
    await sqlbase_create_table.create_faq_table()
    await sqlbase_create_table.create_user_table()

    scheduler.add_job(start_cmd, IntervalTrigger(minutes=1), args=[sqlbase_create_table])
    scheduler.start()
    await dp.start_polling(bot)  # Запускаем бота


if __name__ == "__main__":
    asyncio.run(main())
