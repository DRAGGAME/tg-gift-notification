import asyncio

from aiogram.types import Gifts

from config import bot
from database.db import Sqlbase


async def start_cmd(pool_sqlbase: Sqlbase):

    last_count = await pool_sqlbase.execute_query(f"SELECT count_gifts "
                                               f"FROM settings_table;")

    result: Gifts = await bot.get_available_gifts()
    gift_emojis = [gift for gift in result]
    count = len(gift_emojis[0][1])

    await pool_sqlbase.execute_query(f"UPDATE settings_table SET count_gifts = $1", (count, ))

    users = await pool_sqlbase.execute_query("""SELECT chat_id FROM user_data WHERE purchased = True""")
    if last_count:
        try:
            if count > last_count[0][0]:
                for user in users:
                    message = f"Вышло новых подарков: {count-last_count[0][0]}"
                    await bot.send_message(chat_id=user[0], text=message)
                    await asyncio.sleep(5)
            elif count < last_count[0][0]:
                await bot.send_message(f"Лимитированный подарки закончились: {last_count[0][0]-count}")
            else:
                pass
        except TypeError:
            pass


