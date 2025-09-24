from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, KeyboardButton

from keyboards.fabirc_kb import KeyboardFactory


class InlineProfileMenu(CallbackData, prefix="ProfileMenu"):
    profile_menu_action: str


class InlineAdminMenu(CallbackData, prefix="main_menu"):
    action: str


class InlineSwitchProfile(CallbackData, prefix="switch_profile"):
    profile_action: str
    profile_data: Optional[tuple]


class Payment(CallbackData, prefix="payment"):
    pay: str


class FabricInline(KeyboardFactory):

    def __init__(self):
        super().__init__()

        self.back_button = InlineKeyboardButton(
            text="В главное меню",
            callback_data=InlineAdminMenu(
                action="back",
            ).pack()
        )

    async def inline_main_menu(self):

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
            callback_data=InlineProfileMenu(
                profile_menu_action="begin_price",
            ).pack()
        )

        button_end_price = InlineKeyboardButton(
            text=f"От {price[1]}",
            callback_data=InlineProfileMenu(
                profile_menu_action="end_price",
            ).pack()
        )

        button_begin_gift = InlineKeyboardButton(
            text=f"От {gift[0]}",
            callback_data=InlineProfileMenu(
                profile_menu_action="begin_gift",
            ).pack()
        )

        button_end_gift = InlineKeyboardButton(
            text=f"От {gift[1]}",
            callback_data=InlineProfileMenu(
                profile_menu_action="end_gift",
            ).pack()
        )

        button_replenishment = InlineKeyboardButton(
            text="Пополнение звёзд",
            callback_data=InlineProfileMenu(
                profile_menu_action="replenishment",
            ).pack()
        )

        self.builder_inline.add(button_begin_price, button_end_price)
        self.builder_inline.row(button_begin_gift, button_end_gift)
        self.builder_inline.row(button_replenishment)
        self.builder_inline.row(self.back_button)

        return self.builder_inline.as_markup()

    async def inline_switch_profiles_menu(self, profiles: tuple):
        await self.create_builder_inline()
        button_create_profile = InlineKeyboardButton(
            text="Создать новый профиль",
            callback_data=InlineSwitchProfile(
                profile_action="create_profile",
                profile_data=None
            ).pack()
        )

        await self.builder_inline.add(button_create_profile)

        if profiles:
            for profile in profiles:
                button_tmp_profile = InlineKeyboardButton(
                    text=f"{profile[-1]} {profile[-2]} {profile[-3]}",
                    callback_data=InlineSwitchProfile(
                        profile_action="switch_profile",
                        profile_data=profile,
                    ).pack()
                )
                await self.builder_inline.row(button_tmp_profile)

        await self.builder_inline.row(self.back_button)
        return self.builder_inline.as_markup()

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
