from typing import Tuple

from aiogram.types import Message

from config import bot
from database.admin_operations import AdminOperations
from functions.get_bot_stars import get_bot_stars
from keyboards.menu_fabric import FabricInline


async def answer_answers(admin_database: AdminOperations, answer_fabric_kb: FabricInline,
                         msg_callback: Message, number_profile: int):
    last_profile_data = await admin_database.select_profile(int(number_profile))

    type_regime = "с менее ценных" if last_profile_data[1] == "Up" else "с более ценных"

    begin_price = last_profile_data[-5]
    end_price = last_profile_data[-4]

    gift_count = last_profile_data[2]

    description: str = last_profile_data[-2]
    channel_answer: str = last_profile_data[-1]

    price: Tuple[int, int] = (begin_price, end_price)

    bot_stars = await get_bot_stars()

    keyboard_upd = await answer_fabric_kb.inline_profile_menu(price, gift_count, number_profile)

    await bot.edit_message_text(message_id=msg_callback.message_id, chat_id=msg_callback.chat.id,
                                text="Вы открыли панель действий\n"
                                     "Что вы хотите сделать?\n\n"
                                     "<pre>"
                                     f"Баланс звёзд в боте(ваши): {bot_stars}\n\n"
                                     f"Тип режима покупки: {type_regime}\n"
                                     f"Комменатрий к подарку: {description}\n"
                                     f"Канал для отправки подарков: {channel_answer}"
                                     f"</pre>", reply_markup=keyboard_upd)
