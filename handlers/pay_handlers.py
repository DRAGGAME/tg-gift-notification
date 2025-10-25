from aiogram.fsm.context import FSMContext
from aiogram.types import PreCheckoutQuery, Message

from config import bot
from database.admin_operations import AdminOperations
from aiogram import Router, F

from functions.answer_answers import answer_answers
from keyboards.menu_fabric import FabricInline


class PayHandlers:

    def __init__(self):
        self.bot = bot

        self.router = Router()

        self.admin_database = AdminOperations()

        self.begin_fabric_keyboard = FabricInline()

        self.register_handlers_pay()

    def register_handlers_pay(self):
        self.router.pre_checkout_query.register(self.pre_checkout_handler)

        self.router.message.register(self.successful_payment_handler, F.successful_payment)

    async def pre_checkout_handler(self, pre_checkout_query: PreCheckoutQuery):
        await pre_checkout_query.answer(ok=True)


    async def successful_payment_handler(self, message: Message, state: FSMContext):
        msg_invoice: Message = await state.get_value("msg_invoice")
        msg_callback: Message = await state.get_value("msg_callback")
        number_profile: int = await state.get_value("number_profile")
        print(number_profile)
        await self.admin_database.insert_new_transaction(message.successful_payment.invoice_payload,
                                                  message.successful_payment.telegram_payment_charge_id,
                                                  message.successful_payment.total_amount,)

        await answer_answers(answer_fabric_kb=self.begin_fabric_keyboard,
                             msg_callback=msg_callback,
                             number_profile=number_profile, admin_database=self.admin_database)

        await msg_invoice.delete()