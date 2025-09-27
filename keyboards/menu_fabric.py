from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, KeyboardButton

from keyboards.fabirc_kb import KeyboardFactory


class InlineProfileMenu(CallbackData, prefix="ProfileMenu"):
    profile_menu_action: str
    number_profile: Optional[int]


class InlineAdminMenu(CallbackData, prefix="main_menu"):
    action: str


class InlineSwitchProfile(CallbackData, prefix="switch_profile"):
    profile_action: str
    profile_data: Optional[str]


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

    async def inline_profile_menu(self, price: tuple, gift_count: int, number_profile: int):
        await self.create_builder_inline()
        button_begin_price = InlineKeyboardButton(
            text=f"От {price[0]}⭐",
            callback_data=InlineProfileMenu(
                profile_menu_action="begin_price",
                number_profile=number_profile,
            ).pack()
        )

        button_end_price = InlineKeyboardButton(
            text=f"До {price[1]}⭐",
            callback_data=InlineProfileMenu(
                profile_menu_action="end_price",
                number_profile=number_profile,
            ).pack()
        )

        button_replenishment = InlineKeyboardButton(
            text="Пополнение звёзд⭐",
            callback_data=InlineProfileMenu(
                profile_menu_action="replenishment",
                number_profile=number_profile,
            ).pack()
        )

        button_count_one_gift = InlineKeyboardButton(
            text=f"Кол-во одного подарка: {gift_count}🎁",
            callback_data=InlineProfileMenu(
                profile_menu_action="count_one_gift",
                number_profile=number_profile,
            ).pack()

        )

        button_channel_connection = InlineKeyboardButton(
            text="Подключить канал🪢",
            callback_data=InlineProfileMenu(
                profile_menu_action="channel_connection",
                number_profile=number_profile,
            ).pack()
        )

        button_description = InlineKeyboardButton(
            text="Комментарии💬",
            callback_data=InlineProfileMenu(
                profile_menu_action="description",
                number_profile=number_profile,
            ).pack()
        )

        button_choice_mode = InlineKeyboardButton(
            text="🪛Сменить режим🪛",
            callback_data=InlineProfileMenu(
                profile_menu_action="choice_mode",
                number_profile=number_profile,
            ).pack()
        )

        button_delete_profile = InlineKeyboardButton(
            text="❌Удалить профиль❌",
            callback_data=InlineProfileMenu(
                profile_menu_action="delete_profile",
                number_profile=number_profile,
            ).pack()
        )

        self.builder_inline.add(button_begin_price, button_end_price)
        self.builder_inline.row(button_count_one_gift)
        self.builder_inline.row(button_description, button_channel_connection)
        self.builder_inline.row(button_choice_mode)
        self.builder_inline.row(button_replenishment)
        self.builder_inline.row(button_delete_profile)
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

        self.builder_inline.add(button_create_profile)

        if profiles:
            # Добавить уведомление callback.answer() на ответ к switch_profile
            for profile in profiles:
                symbol = "⬇" if profile[0] == "down" else "⬆️"
                button_tmp_profile = InlineKeyboardButton(
                    text=f"{profile[2]} - {profile[3]}⭐ {profile[1]}🎁 {symbol}",
                    callback_data=InlineSwitchProfile(
                        profile_action="switch_profile",
                        profile_data=f"{profile[-1]}",
                    ).pack()
                )
                self.builder_inline.row(button_tmp_profile)

        self.builder_inline.row(self.back_button)
        return self.builder_inline.as_markup()

    async def back_kb(self):
        await self.create_builder_inline()

        self.builder_inline.add(self.back_button)
        return self.builder_inline.as_markup()

    async def back_profile_menu(self
                                ):
        await self.create_builder_inline()
