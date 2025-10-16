import asyncio
import logging

from aiogram import Dispatcher
from apscheduler.triggers.interval import IntervalTrigger

from config import bot
from database.admin_operations import AdminOperations
from database.create_table import CreateTable
from database.db import Sqlbase
from handlers.back_main_handler import BackMainHandlers
from handlers.main_handlers import MainHandlers
from handlers.switch_profile_handlers import SwitchProfileHandlers
from handlers.upd_gift_and_star import UpdateOptionsHandlers
from handlers.user_handlers import SetupHandlers
from keyboards.menu_fabric import FabricInline
from schedulers.scheduler_object import scheduler
from schedulers.starts import start_cmd

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-4s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

main_fabric_inline = FabricInline()
main_sqlbase = AdminOperations()

"""
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
"""


class TelegramBot:
    """
    Класс главный телеграм-бота
    """

    def __init__(self):
        self.bot = bot
        self.dp = Dispatcher()

        main_handlers = MainHandlers()
        switch_handlers = SwitchProfileHandlers()
        setup_handlers = SetupHandlers()
        update_options_handlers = UpdateOptionsHandlers()
        back_main_handlers = BackMainHandlers()

        self.dp.include_routers(main_handlers.router, switch_handlers.router, setup_handlers.router_setup,
                                update_options_handlers.router, back_main_handlers.router)

    async def run_main(self):
        await Sqlbase.init_pool()

        create_table = CreateTable()

        await create_table.init_pgcrypto()
        await create_table.create_profiles_table()
        await create_table.create_settings_table()
        await create_table.create_transaction_donat()

        sqlbase_admin = AdminOperations()
        scheduler.add_job(start_cmd, IntervalTrigger(seconds=120), args=[sqlbase_admin])
        scheduler.start()

        await self.dp.start_polling(self.bot, skip_updates=True)
        await Sqlbase.close_pool()


async def main():
    await Sqlbase.init_pool()
    tg_bot = TelegramBot()

    await tg_bot.run_main()


if __name__ == "__main__":
    asyncio.run(main())
