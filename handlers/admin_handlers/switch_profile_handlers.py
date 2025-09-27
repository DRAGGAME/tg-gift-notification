from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from database.admin_operations import AdminOperations
from filters.check_admin import CheckAdminDefault
from functions.get_bot_stars import get_bot_stars
from keyboards.menu_fabric import InlineSwitchProfile, FabricInline

router_for_switch = Router()
sqlbase_for_switch = AdminOperations()
keyboard_for_switch = FabricInline()

router_for_switch.callback_query.filter(CheckAdminDefault(sqlbase_for_switch))

@router_for_switch.callback_query(InlineSwitchProfile.filter(F.profile_action=="switch_profile"))
async def switch_profile_callback(callback: CallbackQuery, callback_data: CallbackData):
    await sqlbase_for_switch.connect()

    number_profile = callback_data.profile_data
    last_profile_data = await sqlbase_for_switch.select_profile(int(number_profile))

    keyboard_profile = await keyboard_for_switch.inline_profile_menu((+last_profile_data[-5], last_profile_data[-4]),
                                                                     last_profile_data[3], number_profile)
    bot_stars = await get_bot_stars()

    await sqlbase_for_switch.close()
    await callback.message.edit_text("Вы открыли панель действий\n"
                         "Что вы хотите сделать?\n\n"
                         "<pre>"
                         f"Баланс звёзд в боте(ваши): {bot_stars}"
                         f"</pre>", reply_markup=keyboard_profile)
    await callback.answer()

@router_for_switch.callback_query(InlineSwitchProfile.filter(F.profile_action=="create_profile"))
async def create_new_profile_callback(callback: CallbackQuery):
    await sqlbase_for_switch.connect()
    try_profile = await sqlbase_for_switch.insert_profile()
    if try_profile:
        keyboard_profile = await keyboard_for_switch.inline_profile_menu((0, 40),
                                                                         2, try_profile)
        bot_stars = await get_bot_stars()

        await sqlbase_for_switch.close()
        await callback.message.edit_text("Вы открыли панель действий\n"
                             "Что вы хотите сделать?\n\n"
                             "<pre>"
                             f"Баланс звёзд в боте(ваши): {bot_stars}"
                             f"</pre>", reply_markup=keyboard_profile)
        await callback.answer()
    else:
        await callback.answer(text="Максимальное количество профилей - 5", show_alert=True)
