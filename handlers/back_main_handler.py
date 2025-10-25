from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import bot
from database.admin_operations import AdminOperations
from filters.check_admin import CheckAdminCallback
from keyboards.menu_fabric import FabricInline, InlineAdminMenu

class BackMainHandlers:

    def __init__(self):
        self.bot = bot

        self.router = Router()

        self.admin_database = AdminOperations()

        self.back_fabric_keyboard = FabricInline()

        self.register_handlers_back()

    def register_handlers_back(self):
        self.router.callback_query.register(self.back_handler, InlineAdminMenu.filter(F.action == "back"),
                                            CheckAdminCallback(self.admin_database))

    async def back_handler(self, callback: CallbackQuery):
        bot_balance_stars = await bot.get_my_star_balance(request_timeout=30)

        if hasattr(bot_balance_stars, "amount"):
            bot_balance_stars = getattr(bot_balance_stars, "amount")

        keyboard_main = await self.back_fabric_keyboard.inline_main_menu()

        await callback.message.edit_text("Вы открыли панель действий\n"
                             "Что вы хотите сделать?\n\n"
                             "<pre>"
                             f"Баланс звёзд в боте(ваши): {bot_balance_stars}"
                             f"</pre>", reply_markup=keyboard_main)
        await callback.answer()



