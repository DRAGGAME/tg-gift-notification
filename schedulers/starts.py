import numpy as np
from aiogram.types import Gifts, Gift, Sticker, PhotoSize

from config import bot
from database.admin_operations import AdminOperations
from functions.get_bot_stars import get_bot_stars
from logger import logger

async def start_cmd(pool_sqlbase: AdminOperations, all_tmp_message: list=[]):
    sorted_gifts = []
    gifts: Gifts = await bot.get_available_gifts()
    all_premium_gift = {}

    logger.info("Проверка на подарки")
    for info_a_gift in gifts:
        if hasattr(info_a_gift, "total_count"):
            total_count = getattr(info_a_gift, "total_count")

            if total_count is not None:
                end_count = getattr(info_a_gift, "remaining_count")
                price_gift = getattr(info_a_gift, "star_count")
                gift_id = getattr(info_a_gift, "id")

                logger.info("Существует подарок премиум-подарок")

                all_premium_gift[gift_id] = (price_gift, total_count, end_count, )

    if all_premium_gift:
        all_settings = await pool_sqlbase.select_profile_last()
        if not all_settings:
            logger.warning("Нет записи, что существует администратор. ")
            return

        logger.info("Существует запись в БД. Работа продолжена")

        type_regime = all_settings[0][0]
        count_one_gift = all_settings[0][1]
        price_min = all_settings[0][2]
        price_max = all_settings[0][3]
        comment_for_gift = all_settings[0][4]
        channel_for_answer = all_settings[0][5]
        admin_chat_id = all_settings[0][6]

        bot_balance = await get_bot_stars()

        if channel_for_answer == '':
            channel_for_answer = admin_chat_id

        else:
            try:
                channel_for_answer = int(channel_for_answer)
            except ValueError:
                logger.error("Нельзя преобразовать id")
                return

        if channel_for_answer == "0":
            logger.warning("Нет админа")
            return

        if type_regime == "Down":
            logger.info("Активирован режим покупки с высшего до нисшего...")
            all_gifts = [(gift_id, values) for gift_id, values in all_premium_gift.items()
                         if price_min <= values[0] <= price_max]

            if all_gifts:
                logger.info("Доп. проверка на подарки, пройдена")
                prices = np.array([gift[1][0] for gift in all_gifts])
                remaining_counts = np.array([gift[1][2] if gift[1][2] is not None else np.inf for gift in all_gifts])

                # Сортировка от дорогих к дешёвым
                sorted_indices = np.lexsort((remaining_counts, -prices))
                sorted_gifts = [all_gifts[i] for i in sorted_indices]

                for gift in sorted_gifts:
                    gift_id = gift[0]
                    price = gift[1][0]
                    total_count = gift[1][1]
                    remaining_count = gift[1][2]
                    logger.info(f"[Down] ID: {gift_id}, Цена (звёзды): {price}, Total: {total_count}, Осталось: {remaining_count}")

        else:
            logger.info("Активирован режим покупки с низшего до высшего...")
            all_gifts = [(gift_id, values) for gift_id, values in all_premium_gift.items()
                         if price_min <= values[0] <= price_max]

            if all_gifts:
                logger.info("Доп. проверка на подарки, пройдена")
                prices = np.array([gift[1][0] for gift in all_gifts])
                remaining_counts = np.array([gift[1][2] if gift[1][2] is not None else np.inf for gift in all_gifts])

                sorted_indices = np.lexsort((remaining_counts, prices))
                sorted_gifts = [all_gifts[i] for i in sorted_indices]

                for gift in sorted_gifts:
                    gift_id = gift[0]
                    price = gift[1][0]
                    total_count = gift[1][1]
                    remaining_count = gift[1][2]
                    logger.info(f"[Up] ID: {gift_id}, Цена (звёзды): {price}, Total: {total_count}, Осталось: {remaining_count}")


        for gift in sorted_gifts:
            gift_id = gift[0]
            gift_price = gift[1][0]

            for _ in range(count_one_gift):
                next_balance = bot_balance-gift_price
                if next_balance >= 0:

                    bot_balance -= gift_price
                    id_message = await bot.send_gift(gift_id=gift_id,
                                                     chat_id=int(channel_for_answer),
                                                     text=comment_for_gift)
                    all_tmp_message.append(id_message)

                else:
                    next_balance = 0
                    logger.info(f"Бот не может купить подарок. \nХватает ли баланса: {bool(next_balance)}")
                    # msg = await bot.send_message(chat_id=admin_chat_id, text="У бота кончились звёзды")
                    # await bot.delete_message(message_id=msg.message_id, chat_id=admin_chat_id)
                    break




# asyncio.run(start_cmd(pool_sqlbase=AdminOperations()))