from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, Gifts

from config import bot
from database.other_operations import OtherOperation
from keyboards.menu_fabric import FabricInline, InlineMainMenu

start_router = Router()
keyboard_fabric = FabricInline()
start_sqlbase = OtherOperation()


@start_router.message(CommandStart())
async def start_message(message: Message):
    await start_sqlbase.connect()
    result: Gifts = await bot.get_available_gifts()
    gift_emojis = [gift for gift in result]
    print(type(gift_emojis[0][1][0]))
    chat_id = message.chat.id
    check = await start_sqlbase.select_user(str(chat_id))
    if check:
        kb = await keyboard_fabric.builder_reply_choice("Вы соглашаетесь на обработку персональных данных?")
        url_user_politics, url_politics_kond = await start_sqlbase.select_url()
        await message.answer(
            f"Прежде чем вы начнёте пользоваться ботом, пожалуйста, ознакомьтесь и согласитесь с политикой "
            f"конфиденциальности и пользовательским соглашением.\n"
            f'<a href="{url_user_politics}">Пользовательское соглашение</a>\n'
            f'<a href="{url_politics_kond}">Политика конфиденциальности</a>', parse_mode=ParseMode.HTML, reply_markup=kb)
    else:
        kb = await keyboard_fabric.create_inline_main()
        await bot.unpin_all_chat_messages(chat_id=message.chat.id)
        msg = await message.answer("Выберите опцию: ", reply_markup=kb)
        await bot.pin_chat_message(chat_id=message.chat.id, message_id=msg.message_id)


@start_router.message(F.text.lower().startswith('да'))
async def choice(message: Message):
    try:
        kb = await keyboard_fabric.create_inline_main()
        chat_id = message.chat.id

        await start_sqlbase.accept_politics(str(chat_id))

    except ValueError:
        await start_sqlbase.connect()
        kb = await keyboard_fabric.create_inline_main()
        chat_id = message.chat.id

        await start_sqlbase.accept_politics(str(chat_id))
    await start_sqlbase.close()
    await bot.unpin_all_chat_messages(chat_id=message.chat.id)
    msg = await message.answer("Выберите опцию: ", reply_markup=kb)
    await bot.pin_chat_message(chat_id=message.chat.id, message_id=msg.message_id)


@start_router.callback_query(InlineMainMenu.filter(F.action == 'back'))
async def back_inline(callback: CallbackQuery):
    kb = await keyboard_fabric.create_inline_main()
    try:
        await callback.message.edit_text("Выберите опцию", reply_markup=kb)
    except TelegramBadRequest:
        await callback.message.delete()

    await callback.answer()
