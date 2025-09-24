from aiogram import Router
from aiogram.filters import CommandStart

from config import bot
from aiogram.types import Message
from database.admin_operations import AdminOperations
from filters.check_admin import CheckAdminDefault
from filters.check_admin_for_setup import CheckAdminSetup
from keyboards.menu_fabric import FabricInline

router_for_main = Router()
sqlbase_admin = AdminOperations()
keyboard_factory = FabricInline()

router_for_main.message.filter(CheckAdminDefault(sqlbase_admin))
router_for_main.callback_query.filter(CheckAdminDefault(sqlbase_admin))

@router_for_main.message(CommandStart(deep_link=False))
async def start_for_main(message: Message):

    keyboard_start = await keyboard_factory.inline_main_menu()
    bot_balance_stars = await bot.get_my_star_balance(request_timeout=30)
    if hasattr(bot_balance_stars, "amount"):
        bot_balance_stars = getattr(bot_balance_stars, "amount")

    await message.answer("Вы открыли панель действий\n"
                         "Что вы хотите сделать?\n\n"
                         "<pre>"
                         f"Баланс звёзд в боте(ваши): {bot_balance_stars}"
                         f"</pre>", reply_markup=keyboard_start, protect_content=True)
