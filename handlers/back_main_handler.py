from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import bot
from database.admin_operations import AdminOperations
from filters.check_admin import CheckAdminDefault
from handlers.main_handlers import sqlbase_admin
from keyboards.menu_fabric import FabricInline, InlineAdminMenu

keyboard_fabric = FabricInline()
router_for_back = Router()
sqlbase = AdminOperations()

router_for_back.callback_query.filter(CheckAdminDefault(sqlbase_admin))


@router_for_back.callback_query(InlineAdminMenu.filter(F.action=="back"))
async def back_handler(callback: CallbackQuery):
    bot_balance_stars = await bot.get_my_star_balance(request_timeout=30)

    if hasattr(bot_balance_stars, "amount"):
        bot_balance_stars = getattr(bot_balance_stars, "amount")

    keyboard_main = await keyboard_fabric.inline_main_menu()
    await callback.message.edit_text("Вы открыли панель действий\n"
                         "Что вы хотите сделать?\n\n"
                         "<pre>"
                         f"Баланс звёзд в боте(ваши): {bot_balance_stars}"
                         f"</pre>", reply_markup=keyboard_main)
    await callback.answer()



