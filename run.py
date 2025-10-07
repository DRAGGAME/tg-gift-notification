import asyncio
import logging

from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import PreCheckoutQuery, Message
from apscheduler.triggers.interval import IntervalTrigger

from config import bot, DATABASE, PASSWORD, USER, TG_KEY, HOST
from database.admin_operations import AdminOperations
from database.create_table import CreateTable
from functions.get_bot_stars import get_bot_stars
from handlers.admin_handlers.main_handlers import router_for_main
from handlers.admin_handlers.switch_profile_handlers import router_for_switch
from handlers.admin_handlers.upd_gift_and_star import router_upd
from handlers.back_main_handler import router_for_back
from handlers.user_handlers import router_for_user
from keyboards.menu_fabric import FabricInline
from schedulers.scheduler_object import scheduler
from schedulers.starts import start_cmd

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-4s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

dp = Dispatcher()
main_fabric_inline = FabricInline()
main_sqlbase = AdminOperations()

dp.include_routers(router_for_user, router_for_back, router_for_main, router_for_switch, router_upd)


@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery, state: FSMContext):
    await pre_checkout_query.answer(ok=True)


@dp.message(F.successful_payment)
async def successful_payment_handler(message: Message, state: FSMContext):
    await main_sqlbase.connect()
    msg_invoice: Message = await state.get_value("msg_invoice")
    msg_callback: Message = await state.get_value("msg_callback")
    number_profile: int = await state.get_value("number_profile")

    last_profile_data = await main_sqlbase.select_profile(int(number_profile))

    keyboard_upd = await main_fabric_inline.inline_profile_menu((last_profile_data[-5], last_profile_data[-4]),
                                                                last_profile_data[3], int(number_profile))

    bot_stars = await get_bot_stars()
    await main_sqlbase.insert_new_transaction(message.successful_payment.invoice_payload,
                                              message.successful_payment.telegram_payment_charge_id,
                                              message.successful_payment.total_amount,)
    await main_sqlbase.close()

    await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                text="Вы открыли панель действий\n"
                                     "Что вы хотите сделать?\n\n"
                                     "<pre>"
                                     f"Баланс звёзд в боте(ваши): {bot_stars}\n\n"
                                     f"Тип режима покупки: {last_profile_data[2]}\n"
                                     f"Комменатрий к подарку: {last_profile_data[-2]}\n"
                                     f"Канал для отправки подарков: {last_profile_data[-1]}"
                                     f"</pre>", reply_markup=keyboard_upd)
    await msg_invoice.delete()


async def main():
    print(TG_KEY, HOST, USER, PASSWORD, DATABASE)

    sqlbase_create_table = CreateTable()
    await sqlbase_create_table.connect()
    # await sqlbase_create_table.delete_all()
    await sqlbase_create_table.create_profiles_table()
    await sqlbase_create_table.create_settings_table()
    await sqlbase_create_table.create_transaction_donat()

    sqlbase_admin = AdminOperations()
    scheduler.add_job(start_cmd, IntervalTrigger(seconds=20), args=[sqlbase_admin])
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
