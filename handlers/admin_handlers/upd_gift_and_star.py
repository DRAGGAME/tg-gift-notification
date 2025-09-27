from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods import TelegramMethod
from aiogram.types import CallbackQuery, Message
from pydantic.v1.utils import sequence_like

from config import bot
from database.admin_operations import AdminOperations
from keyboards.menu_fabric import InlineProfileMenu, FabricInline

router_upd = Router()
sqlbase_for_upd = AdminOperations()
fabric_for_upd = FabricInline()


class UpdStar(StatesGroup):
    begin_price = State()
    end_price = State()


class UpdCountGift(StatesGroup):
    gift_count = State()


class UpdDescription(StatesGroup):
    upd_description = State()


class UpdChannelConn(StatesGroup):
    channel = State()


@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action.in_(["begin_price", "end_price"])))
async def upd_begin_price(callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
    begin_or_end_price = callback_data.profile_menu_action
    number_profile = callback_data.number_profile

    await state.clear()
    await state.update_data(number_profile=number_profile)

    await sqlbase_for_upd.connect()

    if begin_or_end_price == "begin_price":
        await state.set_state(UpdStar.begin_price)
        msg_callback = await callback.message.edit_text("Введите цену, от которой бот может начинать покупать подарки")

    else:
        await state.set_state(UpdStar.end_price)
        msg_callback = await callback.message.edit_text("Введите цену, до которой бот может покупать подарки")
    await state.update_data(msg_callback=msg_callback)
    await callback.answer()


@router_upd.message(F.text, UpdStar.end_price)
@router_upd.message(F.text, UpdStar.begin_price)
async def upd_star(message: Message, state: FSMContext):
    await message.delete()
    msg_callback: Message = await state.get_value("msg_callback")
    try:

        try:
            price = int(message.text)

            if price >= 0:
                type_state = await state.get_state()
                number_profile = await state.get_value("number_profile")

                type_state = type_state.split(sep=":")

                await sqlbase_for_upd.update_gift_price(type_state[-1], int(number_profile), int(message.text))
                last_profile_data = await sqlbase_for_upd.select_profile(int(number_profile))
                keyboard_upd = await fabric_for_upd.inline_profile_menu((last_profile_data[-5], last_profile_data[-4]),
                                                                        last_profile_data[3], int(number_profile))

                await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                            text="Панель управления", reply_markup=keyboard_upd)
                await sqlbase_for_upd.close()

            else:
                await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                            text="Введите корректный прайс")
        except ValueError:
            await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                        text="Введите корректное число")
    except TelegramBadRequest:
        pass
    await state.clear()





@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action == "count_one_gift"))
async def count_one_gift_begin(callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
    await sqlbase_for_upd.connect()

    number_profile = callback_data.number_profile

    await state.clear()

    await state.set_state(UpdCountGift.gift_count)
    msg_callback = await callback.message.edit_text("Введите цену, до которой бот может покупать подарки")

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

                await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                            text="Панель управления", reply_markup=keyboard_upd)
                await sqlbase_for_upd.close()
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
    await sqlbase_for_upd.connect()

    await state.set_state(UpdDescription.upd_description)
    msg_callback = await callback.message.edit_text("Введите описание, чтобы изменить описание для подарка")
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

    await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                text="Панель управления", reply_markup=keyboard_upd)
    await sqlbase_for_upd.close()

@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action == "channel_connection"))
async def edit_channel_conn_begin_handler(callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
    await state.clear()
    number_profile = callback_data.number_profile
    await sqlbase_for_upd.connect()

    await state.set_state(UpdChannelConn.channel)
    msg_callback = await callback.message.edit_text("Введите описание, чтобы изменить описание для подарка")
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

    await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                text="Панель управления", reply_markup=keyboard_upd)
    await sqlbase_for_upd.close()

@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action == "choice_mode"))
async def choice_mode_handler(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    await state.clear()
    number_profile = callback_data.number_profile
    await sqlbase_for_upd.connect()
    await sqlbase_for_upd.update_mode(int(number_profile))
    last_profile_data = await sqlbase_for_upd.select_profile(int(number_profile))
    keyboard_upd = await fabric_for_upd.inline_profile_menu((last_profile_data[-5], last_profile_data[-4]),
                                                            last_profile_data[3], int(number_profile))
    try:
        await callback.message.edit_text(text="Панель управления", reply_markup=keyboard_upd)
    except TelegramBadRequest:
        pass
    await sqlbase_for_upd.close()
    await state.clear()
    await callback.answer()

@router_upd.callback_query(InlineProfileMenu.filter(F.profile_menu_action == "delete_profile"))
async def delete_profile(callback: CallbackQuery, state: FSMContext, callback_data: CallbackData):
    number_profile = callback_data.number_profile

    await sqlbase_for_upd.connect()
    await sqlbase_for_upd.delete_profile(int(number_profile))
    await sqlbase_for_upd.close()



    await callback.message.edit_text()
    await callback.answer()
