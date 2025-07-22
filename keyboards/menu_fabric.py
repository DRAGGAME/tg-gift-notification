from typing import Union, Optional

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

    async def create_inline_main(self):
        await self.create_builder_inline()
        faq_button = InlineKeyboardButton(
            text="Тех.поддержка",
            callback_data=InlineMainMenu(
                action="faq",
            ).pack()
        )

        pay_notifications = InlineKeyboardButton(
            text="Купить доступ",
            callback_data=InlineMainMenu(
                action="pay",
            ).pack()
        )

        self.builder_inline.add(faq_button)
        self.builder_inline.add(pay_notifications)

        return self.builder_inline.as_markup()

    async def inline_admin_main_menu(self):

        await self.create_builder_inline()

        button_upd_login = InlineKeyboardButton(
            text="Обновить пароль",
            callback_data=InlineAdminMenu(
                action="UpdPassword"
            ).pack()
        )

        button_edit_politics_url = InlineKeyboardButton(
            text="Ссылка на политику конфиденциальности",
            callback_data=InlineAdminMenu(
                action="UrlPolitics"
            ).pack()
        )

        button_edit_user_url = InlineKeyboardButton(
            text="Ссылка на пользовательское соглашение",
            callback_data=InlineAdminMenu(
                action="UrlUser"
            ).pack()
        )

        button_edit_price = InlineKeyboardButton(
            text="Изменить цену услуги",
            callback_data=InlineAdminMenu(
                action="EditPrice",
            ).pack()
        )

        button_add_faq = InlineKeyboardButton(
            text="Добавить вопрос-ответ",
            callback_data=InlineAdminMenu(
                action="add_faq"
            ).pack()
        )

        button_delete_faq = InlineKeyboardButton(
            text="Удалить вопрос-ответ",
            callback_data=InlineAdminMenu(
                action="delete_faq"
            ).pack()
        )

        button_truncate_faq = InlineKeyboardButton(
            text="Удалить весь FAQ",
            callback_data=InlineAdminMenu(
                action="truncate_faq"
            ).pack()
        )

        button_exit = InlineKeyboardButton(
            text="Выйти из супер-администратора",
            callback_data=InlineAdminMenu(
                action="exit",
            ).pack()
        )

        self.builder_inline.row(button_upd_login)
        self.builder_inline.row(button_edit_politics_url)
        self.builder_inline.row(button_edit_user_url)
        self.builder_inline.row(button_edit_price)
        self.builder_inline.row(button_add_faq)
        self.builder_inline.row(button_delete_faq)
        self.builder_inline.row(button_truncate_faq)
        self.builder_inline.row(button_exit)
        return self.builder_inline.as_markup()

    async def pay_kb(self, sqlbase: Optional[Union[OtherOperation, Sqlbase]], price=-1):
        await self.create_builder_inline()
        if price == -1:
            price = await sqlbase.select_price()

            pay = InlineKeyboardButton(
                text=f"Оплатить {price} XTR",
                pay=True,
            )
        else:
            pay = InlineKeyboardButton(
                text=f"Оплатить {price} XTR",
                pay=True,
            )
        self.builder_inline.add(pay)
        self.builder_inline.row(self.back_button)

        return self.builder_inline.as_markup(), price

    async def donate_kb(self):
        await self.create_builder_inline()

        pay_button = InlineKeyboardButton(
            text="Пожертвование",
            callback_data=InlineMainMenu(
                action="donate"
            ).pack()
        )

        self.builder_inline.add(pay_button, self.back_button)

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
