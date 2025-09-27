from aiogram import Router, F
from aiogram.filters import CommandStart

from config import bot
from aiogram.types import Message, CallbackQuery
from database.admin_operations import AdminOperations
from filters.check_admin import CheckAdminDefault
from filters.check_admin_for_setup import CheckAdminSetup
from keyboards.menu_fabric import FabricInline, InlineAdminMenu, InlineSwitchProfile

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

    await message.delete()
    await message.answer("Вы открыли панель действий\n"
                         "Что вы хотите сделать?\n\n"
                         "<pre>"
                         f"Баланс звёзд в боте(ваши): {bot_balance_stars}"
                         f"</pre>", reply_markup=keyboard_start)

@router_for_main.callback_query(InlineAdminMenu.filter(F.action=="switch_profile"))
async def switch_profile_callback(callback: CallbackQuery):
    await sqlbase_admin.connect()
    all_profiles = await sqlbase_admin.select_profiles()
    kb = await keyboard_factory.inline_switch_profiles_menu(all_profiles)
    await sqlbase_admin.close()
    await callback.message.edit_text("Выберите профиль", reply_markup=kb)
    await callback.answer("Выберите профиль")

@router_for_main.callback_query(InlineSwitchProfile.filter(F.action=="create_profile"))
async def create_profile_callback(callback: CallbackQuery):
    pass
