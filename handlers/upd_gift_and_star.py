import asyncio

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, LabeledPrice
from asyncpg import RestrictViolationError

from config import bot
from database.admin_operations import AdminOperations
from filters.check_admin import CheckAdmin
from functions.answer_answers import answer_answers
from keyboards.menu_fabric import FabricInline, InlineProfileMenu


class UpdStar(StatesGroup):
    begin_price = State()
    end_price = State()


class UpdCountGift(StatesGroup):
    gift_count = State()


class UpdDescription(StatesGroup):
    upd_description = State()


class UpdChannelConn(StatesGroup):
    channel = State()


class Payment(StatesGroup):
    count_for_pay = State()


class UpdateOptionsHandlers:
    def __init__(self):
        self.bot = bot

        self.router = Router()

        self.admin_database = AdminOperations()

        self.begin_fabric_keyboard = FabricInline()

        self.register_handlers_update()

    def register_handlers_update(self):

        self.router.callback_query.register(self.upd_begin_price, InlineProfileMenu.filter(
            F.profile_menu_action.in_(["begin_price", "end_price", "replenishment"])))

        self.router.message.register(self.create_invoice_or_edit_stars, Payment.count_for_pay)
        self.router.message.register(self.create_invoice_or_edit_stars, UpdStar.end_price)
        self.router.message.register(self.create_invoice_or_edit_stars, UpdStar.begin_price)

        self.router.callback_query.register(self.count_one_gift_begin,
                                            InlineProfileMenu.filter(F.profile_menu_action == "count_one_gift"))
        self.router.message.register(self.update_count_gift, F.text, UpdCountGift.gift_count)

        self.router.callback_query.register(self.edit_description_begin_handler,
                                            InlineProfileMenu.filter(F.profile_menu_action == "description"))
        self.router.message.register(self.edit_description, F.text, UpdDescription.upd_description)

        self.router.callback_query.register(self.edit_channel_conn_begin_handler, InlineProfileMenu.filter(F.profile_menu_action == "channel_connection"))
        self.router.message.register(self.edit_channel_conn, F.text, UpdChannelConn.channel)

        self.router.callback_query.register(self.choice_mode_handler, InlineProfileMenu.filter(F.profile_menu_action == "choice_mode"))

        self.router.callback_query.register(self.delete_profile, InlineProfileMenu.filter(F.profile_menu_action == "delete_profile"))

        self.router.callback_query.register(self.activate_profile, InlineProfileMenu.filter(F.profile_menu_action == "activate_profile"))

        self.router.callback_query.register(self.cancel_pay_handler,
                                            InlineProfileMenu.filter(F.profile_menu_action == "cancel_pay"))
        self.router.callback_query.register(self.cancel_pay_handler,
                                            InlineProfileMenu.filter(F.profile_menu_action == "back"))

        self.router.channel_post.register(self.chat_id_handler, Command("chat_id"), CheckAdmin(self.admin_database))


    async def upd_begin_price(self, callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
        begin_or_end_price = callback_data.profile_menu_action
        number_profile = callback_data.id_int

        await state.clear()
        await state.update_data(number_profile=number_profile)

        kb = await self.begin_fabric_keyboard.back_profile_menu(number_profile=number_profile)

        if begin_or_end_price == "begin_price":
            await state.set_state(UpdStar.begin_price)
            msg_callback = await callback.message.edit_text(
                "Введите цену, от которой бот может начинать покупать подарки",
                reply_markup=kb)

        elif begin_or_end_price == "end_price":
            await state.set_state(UpdStar.end_price)
            msg_callback = await callback.message.edit_text("Введите цену, до которой бот может покупать подарки",
                                                            reply_markup=kb)

        else:
            await state.set_state(Payment.count_for_pay)
            msg_callback = await callback.message.edit_text("Введите, сколько вы хотите добавить на баланс бота",
                                                            reply_markup=kb)

        await state.update_data(msg_callback=msg_callback)
        await callback.answer()

    async def create_invoice_or_edit_stars(self, message: Message, state: FSMContext):
        """
        Хэндлер для создания счёта или изменения параметров покупки подарков по звёздам(от скольких до скольких)
        :param message:
        :param state:
        :return:
        """
        msg_callback: Message = await state.get_value("msg_callback")

        try:

            number_profile = await state.get_value("number_profile")

            try:
                price_in_pay = int(message.text)

                if 1_000_000 >= price_in_pay >= 0:
                    await message.delete()

                    type_state = await state.get_state()
                    type_state = type_state.split(sep=":")

                    if type_state[-1] == "count_for_pay":
                        prices = [LabeledPrice(label="XTR", amount=price_in_pay)]
                        msg_invoice = await message.answer_invoice(
                            title="Пополнение бота",
                            description=f"Пополнить бота на {price_in_pay}",
                            prices=prices,
                            provider_token="",
                            payload="New_count",
                            currency="XTR",
                            reply_markup=await self.begin_fabric_keyboard.payment_callback(price_in_pay, number_profile)
                        )
                        await state.clear()
                        await state.update_data(msg_invoice=msg_invoice, number_profile=number_profile)
                        await answer_answers(answer_fabric_kb=self.begin_fabric_keyboard,
                                             msg_callback=msg_callback,
                                             number_profile=number_profile, admin_database=self.admin_database)
                        await message.delete()

                    else:

                        await self.admin_database.update_gift_price(type_state[-1],
                                                                   int(number_profile),
                                                                   int(message.text))  # Для изменения количества звёзд

                        await answer_answers(answer_fabric_kb=self.begin_fabric_keyboard,
                                             msg_callback=msg_callback,
                                             number_profile=number_profile, admin_database=self.admin_database)

                        await state.clear()

                else:
                    await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                                text="Введите корректный прайс(Больше 0 и меньше 1 000 000")

            except ValueError:
                await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                            text="Введите корректное число")
        except TelegramBadRequest:
            pass


    async def count_one_gift_begin(self, callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
        """
        Изменение цен и оплата
        :param callback:
        :param state:
        :param callback_data:
        :return:
        """
        number_profile = callback_data.id_int

        await state.clear()

        await state.set_state(UpdCountGift.gift_count)

        kb = await self.begin_fabric_keyboard.back_profile_menu(number_profile=number_profile)
        msg_callback = await callback.message.edit_text(
            "Введите сколько подарков <b>одного типа</b> может купить бот",
            reply_markup=kb)

        await state.update_data(msg_callback=msg_callback, number_profile=number_profile)
        await callback.answer()

    async def update_count_gift(self, message: Message, state: FSMContext):

        msg_callback: Message = await state.get_value("msg_callback")
        try:

            try:
                number = message.text

                new_count_gift = int(number)

                if new_count_gift >= 0:
                    number_profile = await state.get_value("number_profile")
                    await self.admin_database.update_count_gift(new_count_gift, number_profile)

                    await answer_answers(answer_fabric_kb=self.begin_fabric_keyboard,
                                         msg_callback=msg_callback,
                                         number_profile=number_profile, admin_database=self.admin_database)
                else:
                    await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                                text="Введите корректное число")
            except ValueError:
                await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                            text="Введите корректное число")
        except TelegramBadRequest:
            pass

        await message.delete()
        await state.clear()

    async def edit_description_begin_handler(self, callback: CallbackQuery, state: FSMContext,
                                             callback_data: CallbackData):
        await state.clear()
        number_profile = callback_data.id_int

        await state.set_state(UpdDescription.upd_description)

        kb = await self.begin_fabric_keyboard.back_profile_menu(number_profile=number_profile, activate_clear_description=True)

        msg_callback = await callback.message.edit_text("Введите описание, чтобы изменить описание для подарка",
                                                        reply_markup=kb)
        await state.update_data(msg_callback=msg_callback, number_profile=number_profile)

        await callback.answer()

    async def edit_description(self, message: Message, state: FSMContext):
        msg_callback: Message = await state.get_value("msg_callback")
        number_profile = await state.get_value("number_profile")
        description = message.text

        await self.admin_database.update_description(description, number_profile)

        await message.delete()
        await answer_answers(answer_fabric_kb=self.begin_fabric_keyboard,
                             msg_callback=msg_callback,
                             number_profile=number_profile, admin_database=self.admin_database)

    async def edit_channel_conn_begin_handler(self, callback: CallbackQuery, state: FSMContext,
                                              callback_data: CallbackData):
        await state.clear()
        number_profile = callback_data.id_int

        kb = await self.begin_fabric_keyboard.back_profile_menu(number_profile=number_profile, activate_channel_clear=True)
        await state.set_state(UpdChannelConn.channel)
        msg_callback = await callback.message.edit_text("Введите описание, чтобы изменить описание для подарка",
                                                        reply_markup=kb)

        await state.update_data(msg_callback=msg_callback, number_profile=number_profile)

        await callback.answer()

    async def edit_channel_conn(self, message: Message, state: FSMContext):
        msg_callback: Message = await state.get_value("msg_callback")
        number_profile = await state.get_value("number_profile")

        channel_connection = message.text

        await self.admin_database.update_channel_for_answer(channel_connection, number_profile)
        await message.delete()

        await answer_answers(answer_fabric_kb=self.begin_fabric_keyboard,
                             msg_callback=msg_callback,
                             number_profile=number_profile, admin_database=self.admin_database)

    async def choice_mode_handler(self, callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
        await state.clear()
        number_profile = callback_data.id_int

        await self.admin_database.update_mode(int(number_profile))


        try:
            await answer_answers(answer_fabric_kb=self.begin_fabric_keyboard,
                                 msg_callback=callback.message,
                                 number_profile=number_profile, admin_database=self.admin_database)
        except TelegramBadRequest:
            pass

        await state.clear()
        await callback.answer()

    async def delete_profile(self, callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
        await state.clear()

        number_profile = callback_data.id_int

        try:
            await self.admin_database.delete_profile(int(number_profile))

        except RestrictViolationError:
            await callback.answer(text="Нельзя удалить активированный профиль", show_alert=True)
            return

        last_profile_data = await self.admin_database.select_profiles()
        keyboard_nach_delete = await self.begin_fabric_keyboard.inline_switch_profiles_menu(last_profile_data)

        await callback.message.edit_text(text="Выберите профиль", reply_markup=keyboard_nach_delete)
        await callback.answer()

    async def activate_profile(self, callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
        await state.clear()

        number_profile = callback_data.id_int

        await self.admin_database.activate_profile(number_profile)

        try:
            await answer_answers(answer_fabric_kb=self.begin_fabric_keyboard,
                                 msg_callback=callback.message,
                                 number_profile=number_profile, admin_database=self.admin_database)
        except TelegramBadRequest:
            pass

        await state.clear()
        await callback.answer()

    async def cancel_pay_handler(self, callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):

        number_profile = callback_data.id_int
        type_cancels = callback_data.profile_menu_action

        if type_cancels == "cancel_pay":
            msg_invoice: Message = await state.get_value("msg_invoice")
            await msg_invoice.delete()
            await state.clear()
            return
        try:
            await answer_answers(answer_fabric_kb=self.begin_fabric_keyboard,
                                 msg_callback=callback.message,
                                 number_profile=number_profile, admin_database=self.admin_database)
        except TelegramBadRequest:
            pass

    async def chat_id_handler(self, message: Message):
        await message.delete()
        msg = await message.answer(f"Айди чата: <code>{message.chat.id}</code>\n\n"
                                   f"У вас минута на копирование")
        await asyncio.sleep(60)
        await msg.delete()

