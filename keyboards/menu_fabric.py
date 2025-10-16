from idlelib.configdialog import is_int
from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, KeyboardButton

from keyboards.fabirc_kb import KeyboardFactory


class InlineProfileMenu(CallbackData, prefix="ProfileMenu"):
    profile_menu_action: str
    id_int: Optional[int]


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
            text="📃Переключить профиль📃",
            callback_data=InlineAdminMenu(
                action="switch_profile",
            ).pack()
        )

        button_clear_settings = InlineKeyboardButton(
            text="🖥️Заводские настройки🖥️",
            callback_data=InlineAdminMenu(
                action="clear_settings",
            ).pack()
        )

        self.builder_inline.row(button_profiles)
        self.builder_inline.row(button_clear_settings)
        return self.builder_inline.as_markup()

    async def inline_profile_menu(self, price: tuple, gift_count: int, id_integer: int):
        await self.create_builder_inline()
        button_begin_price = InlineKeyboardButton(
            text=f"От {price[0]}⭐",
            callback_data=InlineProfileMenu(
                profile_menu_action="begin_price",
                id_int=id_integer,
            ).pack()
        )

        button_end_price = InlineKeyboardButton(
            text=f"До {price[1]}⭐",
            callback_data=InlineProfileMenu(
                profile_menu_action="end_price",
                id_int=id_integer,
            ).pack()
        )

        button_replenishment = InlineKeyboardButton(
            text="⭐Пополнение звёзд⭐",
            callback_data=InlineProfileMenu(
                profile_menu_action="replenishment",
                id_int=id_integer,
            ).pack()
        )

        button_count_one_gift = InlineKeyboardButton(
            text=f"Кол-во одного подарка: {gift_count}🎁",
            callback_data=InlineProfileMenu(
                profile_menu_action="count_one_gift",
                id_int=id_integer,
            ).pack()

        )

        button_channel_connection = InlineKeyboardButton(
            text="Подключить канал🪢",
            callback_data=InlineProfileMenu(
                profile_menu_action="channel_connection",
                id_int=id_integer,
            ).pack()
        )

        button_description = InlineKeyboardButton(
            text="Комментарии💬",
            callback_data=InlineProfileMenu(
                profile_menu_action="description",
                id_int=id_integer,
            ).pack()
        )

        button_choice_mode = InlineKeyboardButton(
            text="🪛Сменить режим🪛",
            callback_data=InlineProfileMenu(
                profile_menu_action="choice_mode",
                id_int=id_integer,
            ).pack()
        )

        button_delete_profile = InlineKeyboardButton(
            text="❌Удалить профиль❌",
            callback_data=InlineProfileMenu(
                profile_menu_action="delete_profile",
                id_int=id_integer,
            ).pack()
        )

        button_activate_profile = InlineKeyboardButton(
            text="🔛Активировать профиль🔛",
            callback_data=InlineProfileMenu(
                profile_menu_action="activate_profile",
                id_int=id_integer,
            ).pack()
        )

        self.builder_inline.add(button_begin_price, button_end_price)
        self.builder_inline.row(button_count_one_gift)
        self.builder_inline.row(button_description, button_channel_connection)
        self.builder_inline.row(button_choice_mode)
        self.builder_inline.row(button_activate_profile)
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
                print(profile[0])
                symbol = "⬇" if profile[0] == "Down" else "⬆️"
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

    async def back_profile_menu(self, number_profile: int, activate_channel_clear: bool=False, activate_clear_description: bool=False):
        await self.create_builder_inline()
        button_back = InlineKeyboardButton(
            text="Возврат",
            callback_data=InlineProfileMenu(
                profile_menu_action="back",
                id_int=number_profile
            ).pack()
        )

        if activate_channel_clear:

            button_channel_clear = InlineKeyboardButton(
                text="Сбросить канал",
                callback_data=InlineProfileMenu(
                    profile_menu_action="channel_clear",
                    id_int=number_profile
                ).pack()
            )
            self.builder_inline.row(button_channel_clear)

        elif activate_clear_description:
            button_description_clear = InlineKeyboardButton(
                text="Сбросить подпись",
                callback_data=InlineProfileMenu(
                    profile_menu_action="description_clear",
                    id_int=number_profile
                ).pack()
            )
            self.builder_inline.row(button_description_clear)

        self.builder_inline.row(button_back)

        return self.builder_inline.as_markup()


    async def payment_callback(self, price: int, number_profile: int):
        await self.create_builder_inline()

        pay = InlineKeyboardButton(
            text=f"Оплатить {price} XTR",
            pay=True,
        )

        button_back = InlineKeyboardButton(
            text="Отмена платежа",
            callback_data=InlineProfileMenu(
                profile_menu_action="cancel_pay",
                id_int=number_profile
            ).pack()
        )

        self.builder_inline.add(pay)
        self.builder_inline.row(button_back)

        return self.builder_inline.as_markup()



