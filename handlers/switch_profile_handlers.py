from typing import Tuple

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from config import bot
from database.admin_operations import AdminOperations
from database.other_operations import OtherOperation
from functions.get_bot_stars import get_bot_stars
from keyboards.menu_fabric import InlineSwitchProfile, FabricInline


class SwitchProfileHandlers:

    def __init__(self):
        self.bot = bot

        self.router = Router()

        self.database = OtherOperation()
        self.admin_database = AdminOperations()

        self.switch_fabric_keyboard = FabricInline()

        self.register_handlers_switch()

    def register_handlers_switch(self):
        self.router.callback_query.register(self.switch_profile_callback,
                                            InlineSwitchProfile.filter(F.profile_action))

    async def switch_profile_callback(self, callback: CallbackQuery, callback_data: CallbackData):
        bot_stars = await get_bot_stars()
        print(callback_data.profile_action)
        if callback_data.profile_action == "switch_profile":
            number_profile = callback_data.profile_data

            last_profile_data = await self.admin_database.select_profile(int(number_profile))

            type_regime = "с менее ценных" if last_profile_data[1] == "Up" else "с более ценных"
            try_profile = last_profile_data[0]
            begin_price = last_profile_data[3]
            end_price = last_profile_data[4]

            gift_count = last_profile_data[2]

            description: str = last_profile_data[6]
            channel_answer: str = last_profile_data[7]

            price: Tuple[int, int] = (begin_price, end_price)

            activation = '🟢' if last_profile_data[-4] == number_profile else '🔴'


        else:
            try_profile, count_profile = await self.admin_database.insert_profile("")

            if count_profile == 5:
                await callback.answer("Вы достигли максимального количества профилей", show_alert=True)
                return

            type_regime = "с менее ценных"

            price: Tuple[int, int] = (0, 1000)
            gift_count: int = 2

            description: str = ""
            channel_answer: str = ""
            activation = ''

        keyboard_profile = await self.switch_fabric_keyboard.inline_profile_menu(price=price, gift_count=gift_count,
                                                                                 id_integer=try_profile, activation=activation)

        await callback.message.edit_text(text="Вы открыли панель действий\n"
                                              "Что вы хотите сделать?\n\n"
                                              "<pre>"
                                              f"Баланс звёзд в боте(ваши): {bot_stars}\n\n"
                                              f"Тип режима покупки(начиная): {type_regime}\n"
                                              f"Комменатрий к подарку: {description}\n"
                                              f"Канал для отправки подарков: {channel_answer}"
                                              f"</pre>", reply_markup=keyboard_profile)
        await callback.answer()
