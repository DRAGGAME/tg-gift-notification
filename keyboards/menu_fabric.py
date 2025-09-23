from typing import Union, Optional, Tuple

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, KeyboardButton

from database.db import Sqlbase
from database.other_operations import OtherOperation
from keyboards.fabirc_kb import KeyboardFactory


class InlineMainMenu(CallbackData, prefix="main_menu"):
    action: str


class InlineAdminMenu(CallbackData, prefix="main_menu"):
    action: str


class Payment(CallbackData, prefix="payment"):
    pay: str


class FabricInline(KeyboardFactory):

    def __init__(self):
        super().__init__()

        self.back_button = InlineKeyboardButton(
            text="В главное меню",
            callback_data=InlineMainMenu(
                action="back",
            ).pack()
        )

    async def create_replenishment_keyboard(self):

        pay_notifications = InlineKeyboardButton(
            text="Пополнить",
            callback_data=InlineMainMenu(
                action="replenishment",
            ).pack()
        )

        self.builder_inline.add(pay_notifications)

        return self.builder_inline.as_markup()

    async def inline_main_menu(self, price: tuple, gift: tuple):

        await self.create_builder_inline()

        button_profiles = InlineKeyboardButton(
            text="Переключить профиль",
            callback_data=InlineAdminMenu(
                action="switch_profile",
            ).pack()
        )

        button_clear_settings = InlineKeyboardButton(
            text="Заводские настройки",
            callback_data=InlineAdminMenu(
                action="clear_settings",
            ).pack()
        )

        self.builder_inline.row(button_profiles)
        self.builder_inline.row(button_clear_settings)
        return self.builder_inline.as_markup()

    async def inline_profile_menu(self, price: tuple, gift: tuple):
        await self.create_builder_inline()
        button_begin_price = InlineKeyboardButton(
            text=f"От {price[0]}",
            callback_data=InlineAdminMenu(
                action="begin_price",
            ).pack()
        )

        button_end_price = InlineKeyboardButton(
            text=f"От {price[1]}",
            callback_data=InlineAdminMenu(
                action="begin_price",
            ).pack()
        )

        button_begin_gift = InlineKeyboardButton(
            text=f"От {gift[0]}",
            callback_data=InlineAdminMenu(
                action="begin_price",
            ).pack()
        )

        button_end_gift = InlineKeyboardButton(
            text=f"От {gift[1]}",
            callback_data=InlineAdminMenu(
                action="begin_price",
            ).pack()
        )

        button_replenishment = InlineKeyboardButton(
            text="Пополнение звёзд",
            callback_data=InlineAdminMenu(
                action="replenishment",
            ).pack()
        )

        return

    async def inline_switch_profiles_menu(self, profiles: tuple):
        if profiles:
            for profile in profiles:
                pass # Изменить



    async def back_kb(self):
        await self.create_builder_inline()

        self.builder_inline.add(self.back_button)
        return self.builder_inline.as_markup()

    async def stop(self):
        await self.create_builder_reply()

        self.builder_reply.add(KeyboardButton(text="Стоп"))

        return self.builder_reply.as_markup(resize_keyboard=True,
                                            input_field_placeholder='Выберите сообщение, которое вы хотите изменить',
                                            is_persistent=True)
