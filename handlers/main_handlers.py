from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart

from config import bot
from aiogram.types import Message, CallbackQuery
from database.admin_operations import AdminOperations
from database.other_operations import OtherOperation
from filters.check_admin import CheckAdmin
from keyboards.menu_fabric import FabricInline, InlineAdminMenu, InlineSwitchProfile
from schedulers.scheduler_object import scheduler


class MainHandlers:

    def __init__(self):
        self.bot = bot

        self.router = Router()

        self.database = OtherOperation()
        self.admin_database = AdminOperations()

        self.begin_fabric_keyboard = FabricInline()

        self.register_handlers_start()

    def register_handlers_start(self):
        self.router.message.register(self.start_for_main, CommandStart(deep_link=False), CheckAdmin(self.admin_database))

        self.router.callback_query.register(self.switch_profile_callback, InlineAdminMenu.filter(F.action=="switch_profile"))

        self.router.callback_query.register(self.delete_profile, InlineAdminMenu.filter(F.action=="clear_settings"))

    async def start_for_main(self, message: Message):

        keyboard_start = await self.begin_fabric_keyboard.inline_main_menu()

        bot_balance_stars = await bot.get_my_star_balance(request_timeout=30)

        if hasattr(bot_balance_stars, "amount"):
            bot_balance_stars = getattr(bot_balance_stars, "amount")

        await message.delete()

        await message.answer("Вы открыли панель действий\n"
                             "Что вы хотите сделать?\n\n"
                             "<pre>"
                             f"Баланс звёзд в боте(ваши): {bot_balance_stars}"
                             f"</pre>", reply_markup=keyboard_start)

    async def switch_profile_callback(self, callback: CallbackQuery):
        all_profiles = await self.admin_database.select_profiles()
        kb = await self.begin_fabric_keyboard.inline_switch_profiles_menu(all_profiles)
        await callback.message.edit_text("Выберите профиль", reply_markup=kb)
        await callback.answer("Выберите профиль")

    async def delete_profile(self, callback: CallbackQuery):
        from database.create_table import CreateTable

        sqlbase_table = CreateTable()
        scheduler.pause()

        await sqlbase_table.delete_all_table()

        await sqlbase_table.create_profiles_table()
        await sqlbase_table.create_settings_table()
        await sqlbase_table.create_transaction_donat()
        try:
            await callback.message.delete()

            scheduler.resume()

            await callback.answer("ВСЁ СБРОШЕНО", show_alert=True)
        except TelegramBadRequest:
            await callback.message.edit_text("Всё сброшено")

            scheduler.resume()
            await callback.answer("ВСЁ СБРОШЕНО", show_alert=True)

