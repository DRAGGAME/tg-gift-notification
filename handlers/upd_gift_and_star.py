from typing import Tuple

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, LabeledPrice

from config import bot
from database.admin_operations import AdminOperations
from functions.get_bot_stars import get_bot_stars
from keyboards.menu_fabric import FabricInline, InlineProfileMenu
from logger import logger


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

        self.router.message.register(self.create_invoice_or_edit_prices, UpdCountGift.gift_count)
        self.router.message.register(self.create_invoice_or_edit_prices, UpdStar.end_price)
        self.router.message.register(self.create_invoice_or_edit_prices, UpdStar.begin_price)

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
            await state.set_state(UpdCountGift.gift_count)
            msg_callback = await callback.message.edit_text("Введите, сколько вы хотите добавить на баланс бота",
                                                            reply_markup=kb)

        await state.update_data(msg_callback=msg_callback)
        await callback.answer()

    async def create_invoice_or_edit_prices(self, message: Message, state: FSMContext):
        """
        Хэндлер для создания счёта или изменения параметров покупки звёзд(от скольких до скольких)
        :param message:
        :param state:
        :return:
        """
        msg_callback: Message = await state.get_value("msg_callback")

        try:

            number_profile = await state.get_value("number_profile")

            last_profile_data = await self.admin_database.select_profile(int(number_profile))
            type_regime = "с менее ценных" if last_profile_data[2] == "Up" else "с более ценных"

            begin_price = last_profile_data[-5]
            end_price = last_profile_data[-4]

            gift_count = last_profile_data[3]
            try_profile = last_profile_data[0]

            description: str = last_profile_data[-2]
            channel_answer: str = last_profile_data[-1]

            bot_stars = await get_bot_stars()

            try:
                price = int(message.text)

                if price >= 0 <= 1_000_000:
                    type_state = await state.get_state()
                    type_state = type_state.split(sep=":")

                    if type_state[-1] == "gift_count":
                        prices = [LabeledPrice(label="XTR", amount=price)]
                        msg_invoice = await message.answer_invoice(
                            title="Пополнение бота",
                            description=f"Пополнить бота на {price}",
                            prices=prices,
                            provider_token="",
                            payload="New_count",
                            currency="XTR",
                            reply_markup=await self.begin_fabric_keyboard.payment_callback(price, number_profile)
                        )

                        await state.update_data(msg_invoice=msg_invoice, number_profile=number_profile)
                        await message.delete()

                    else:

                        price_dict: dict = await self.admin_database.update_gift_price(type_state[-1],
                                                                                       int(number_profile),
                                                                                       int(message.text))  # Для изменения количества звёзд

                        if price_dict["begin_price"]:
                            begin_price = price_dict["begin_price"]

                        elif price_dict["end_price"]:
                            end_price = price_dict["end_price"]

                        else:
                            logger.error("Ошибка преобразования цен")
                            return

                    price: Tuple[int, int] = (begin_price, end_price)

                    keyboard_upd = await self.begin_fabric_keyboard.inline_profile_menu(
                        price=price, gift_count=gift_count, id_integer=try_profile)

                    await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                                text="Вы открыли панель действий\n"
                                                     "Что вы хотите сделать?\n\n"
                                                     "<pre>"
                                                     f"Баланс звёзд в боте(ваши): {bot_stars}\n\n"
                                                     f"Тип режима покупки: {type_regime}\n"
                                                     f"Комменатрий к подарку: {description}\n"
                                                     f"Канал для отправки подарков: {channel_answer}"
                                                     f"</pre>", reply_markup=keyboard_upd)

                    await state.clear()

                else:
                    await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                                text="Введите корректный прайс(Больше 0 и меньше 1 000 000")

            except ValueError:
                await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                            text="Введите корректное число")
        except TelegramBadRequest:
            pass

        await message.delete()


"""


@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action == "count_one_gift"))
async def count_one_gift_begin(callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
    

    number_profile = callback_data.number_profile

    await state.clear()

    await state.set_state(UpdCountGift.gift_count)
    kb = await fabric_for_upd.back_profile_menu(number_profile=number_profile)
    msg_callback = await callback.message.edit_text("Введите цену, до которой бот может покупать подарки",
                                                    reply_markup=kb)

    await state.update_data(msg_callback=msg_callback, number_profile=number_profile)
    await callback.answer()


@router_upd.message(F.text, UpdCountGift.gift_count)
async def update_count_gift(message: Message, state: FSMContext):
    await message.delete()

    msg_callback: Message = await state.get_value("msg_callback")
    try:

        try:
            number = message.text

            new_count_gift = int(number)

            if new_count_gift >= 0:
                number_profile = await state.get_value("number_profile")
                await sqlbase_for_upd.update_count_gift(new_count_gift, number_profile)
                last_profile_data = await sqlbase_for_upd.select_profile(int(number_profile))
                keyboard_upd = await fabric_for_upd.inline_profile_menu((last_profile_data[-5], last_profile_data[-4]),
                                                                        last_profile_data[3], int(number_profile))

                bot_stars = await get_bot_stars()

                await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                            text="Вы открыли панель действий\n"
                                                 "Что вы хотите сделать?\n\n"
                                                 "<pre>"
                                                 f"Баланс звёзд в боте(ваши): {bot_stars}\n\n"
                                                 f"Тип режима покупки: {last_profile_data[2]}\n"
                                                 f"Комменатрий к подарку: {last_profile_data[-2]}\n"
                                                 f"Канал для отправки подарков: {last_profile_data[-1]}"
                                                 f"</pre>", reply_markup=keyboard_upd)
                
            else:
                await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                            text="Введите корректное число")
        except ValueError:
            await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                        text="Введите корректное число")
    except TelegramBadRequest:
        pass

    await state.clear()


@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action == "description"))
async def edit_description_begin_handler(callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
    await state.clear()
    number_profile = callback_data.number_profile
    

    await state.set_state(UpdDescription.upd_description)
    kb = await fabric_for_upd.back_profile_menu(number_profile=number_profile)
    msg_callback = await callback.message.edit_text("Введите описание, чтобы изменить описание для подарка",
                                                    reply_markup=kb)
    await state.update_data(msg_callback=msg_callback, number_profile=number_profile)

    await callback.answer()


@router_upd.message(F.text, UpdDescription.upd_description)
async def edit_description(message: Message, state: FSMContext):
    msg_callback: Message = await state.get_value("msg_callback")
    number_profile = await state.get_value("number_profile")
    description = message.text
    await message.delete()

    await sqlbase_for_upd.update_description(description, number_profile)
    last_profile_data = await sqlbase_for_upd.select_profile(int(number_profile))
    keyboard_upd = await fabric_for_upd.inline_profile_menu((last_profile_data[-5], last_profile_data[-4]),
                                                            last_profile_data[3], int(number_profile))

    bot_stars = await get_bot_stars()

    await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                text="Вы открыли панель действий\n"
                                     "Что вы хотите сделать?\n\n"
                                     "<pre>"
                                     f"Баланс звёзд в боте(ваши): {bot_stars}\n\n"
                                     f"Тип режима покупки: {last_profile_data[2]}\n"
                                     f"Комменатрий к подарку: {last_profile_data[-2]}\n"
                                     f"Канал для отправки подарков: {last_profile_data[-1]}"
                                     f"</pre>", reply_markup=keyboard_upd)
    


@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action == "channel_connection"))
async def edit_channel_conn_begin_handler(callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
    await state.clear()
    number_profile = callback_data.number_profile
    
    kb = await fabric_for_upd.back_profile_menu(number_profile=number_profile)
    await state.set_state(UpdChannelConn.channel)
    msg_callback = await callback.message.edit_text("Введите описание, чтобы изменить описание для подарка",
                                                    reply_markup=kb)
    await state.update_data(msg_callback=msg_callback, number_profile=number_profile)

    await callback.answer()


@router_upd.message(F.text, UpdChannelConn.channel)
async def edit_channel_conn(message: Message, state: FSMContext):
    msg_callback: Message = await state.get_value("msg_callback")
    number_profile = await state.get_value("number_profile")
    channel_connection = message.text
    await message.delete()

    await sqlbase_for_upd.update_channel_for_answer(channel_connection, number_profile)
    last_profile_data = await sqlbase_for_upd.select_profile(int(number_profile))
    keyboard_upd = await fabric_for_upd.inline_profile_menu((last_profile_data[-5], last_profile_data[-4]),
                                                            last_profile_data[3], int(number_profile))

    bot_stars = await get_bot_stars()

    await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                text="Вы открыли панель действий\n"
                                     "Что вы хотите сделать?\n\n"
                                     "<pre>"
                                     f"Баланс звёзд в боте(ваши): {bot_stars}\n\n"
                                     f"Тип режима покупки: {last_profile_data[2]}\n"
                                     f"Комменатрий к подарку: {last_profile_data[-2]}\n"
                                     f"Канал для отправки подарков: {last_profile_data[-1]}"
                                     f"</pre>", reply_markup=keyboard_upd)
    


@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action == "choice_mode"))
async def choice_mode_handler(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    await state.clear()
    number_profile = callback_data.number_profile
    
    await sqlbase_for_upd.update_mode(int(number_profile))
    last_profile_data = await sqlbase_for_upd.select_profile(int(number_profile))
    keyboard_upd = await fabric_for_upd.inline_profile_menu((last_profile_data[-5], last_profile_data[-4]),
                                                            last_profile_data[3], int(number_profile))
    bot_stars = await get_bot_stars()

    try:
        await callback.message.edit_text(text="Вы открыли панель действий\n"
                                              "Что вы хотите сделать?\n\n"
                                              "<pre>"
                                              f"Баланс звёзд в боте(ваши): {bot_stars}\n\n"
                                              f"Тип режима покупки: {last_profile_data[2]}\n"
                                              f"Комменатрий к подарку: {last_profile_data[-2]}\n"
                                              f"Канал для отправки подарков: {last_profile_data[-1]}"
                                              f"</pre>", reply_markup=keyboard_upd)
    except TelegramBadRequest:
        pass
    
    await state.clear()
    await callback.answer()


@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action == "delete_profile"))
async def delete_profile(callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
    await state.clear()

    number_profile = callback_data.number_profile

    
    try:
        await sqlbase_for_upd.delete_profile(int(number_profile))
    except ForeignKeyViolationError:
        await callback.answer(text="Нельзя удалить активированный профиль", show_alert=True)
        return
    last_profile_data = await sqlbase_for_upd.select_profiles()
    keyboard_nach_delete = await fabric_for_upd.inline_switch_profiles_menu(last_profile_data)
    

    await callback.message.edit_text(text="Выберите профиль", reply_markup=keyboard_nach_delete)
    await callback.answer()


@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action == "activate_profile"))
async def activate_profile(callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
    await state.clear()
    
    number_profile = callback_data.number_profile

    await sqlbase_for_upd.activate_profile(number_profile)
    last_profile_data = await sqlbase_for_upd.select_profile(int(number_profile))
    keyboard_upd = await fabric_for_upd.inline_profile_menu((last_profile_data[-5], last_profile_data[-4]),
                                                            last_profile_data[3], int(number_profile))
    bot_stars = await get_bot_stars()
    try:
        await callback.message.edit_text(text="Вы открыли панель действий\n"
                                              "Что вы хотите сделать?\n\n"
                                              "<pre>"
                                              f"Баланс звёзд в боте(ваши): {bot_stars}\n\n"
                                              f"Тип режима покупки: {last_profile_data[2]}\n"
                                              f"Комменатрий к подарку: {last_profile_data[-2]}\n"
                                              f"Канал для отправки подарков: {last_profile_data[-1]}"
                                              f"</pre>", reply_markup=keyboard_upd)
    except TelegramBadRequest:
        pass
    
    await state.clear()
    await callback.answer()

@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action == "cancel_pay"))
@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action == "back"))
async def cancel_pay_handler(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    
    number_profile = callback_data.number_profile
    type_cancels = callback_data.profile_menu_action

    if type_cancels == "cancel_pay":
        msg_invoice: Message = await state.get_value("msg_invoice")
        await msg_invoice.delete()
        await state.clear()
        return

    last_profile_data = await sqlbase_for_upd.select_profile(int(number_profile))
    keyboard_upd = await fabric_for_upd.inline_profile_menu((last_profile_data[-5], last_profile_data[-4]),
                                                            last_profile_data[3], int(number_profile))
    bot_stars = await get_bot_stars()

    await state.clear()
    
    try:
        await callback.message.edit_text(text="Вы открыли панель действий\n"
                                              "Что вы хотите сделать?\n\n"
                                              "<pre>"
                                              f"Баланс звёзд в боте(ваши): {bot_stars}\n\n"
                                              f"Тип режима покупки: {last_profile_data[2]}\n"
                                              f"Комменатрий к подарку: {last_profile_data[-2]}\n"
                                              f"Канал для отправки подарков: {last_profile_data[-1]}"
                                              f"</pre>", reply_markup=keyboard_upd)
    except TelegramBadRequest:
        pass
"""
