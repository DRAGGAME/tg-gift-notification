from typing import Union

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from database.db import Sqlbase
from database.other_operations import OtherOperation
from keyboards.fabirc_kb import KeyboardFactory


class InlineMainMenu(CallbackData, prefix="main_menu"):
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

    async def pay_kb(self, sqlbase: Union[OtherOperation, Sqlbase]):
        await self.create_builder_inline()
        price = await sqlbase.select_price()

        pay = InlineKeyboardButton(
            text=f"Оплатить {price} XTR",
            pay=True,
        )
        self.builder_inline.add(pay)
        self.builder_inline.row(self.back_button)

        return self.builder_inline.as_markup(), price

    async def back_kb(self):
        await self.create_builder_inline()

        self.builder_inline.add(self.back_button)
        return self.builder_inline.as_markup()
