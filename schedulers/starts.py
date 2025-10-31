import numpy as np
from aiogram.types import Gifts
from config import bot
from database.admin_operations import AdminOperations
from functions.get_bot_stars import get_bot_stars
from logger import logger

async def start_cmd(pool_sqlbase: AdminOperations, all_tmp_message: list = []):
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

                all_premium_gift[gift_id] = (price_gift, total_count, end_count)

    if not all_premium_gift:
        logger.warning("Нет лимитированных подарков.")
        return

    all_settings = await pool_sqlbase.select_profile_last()
    if not all_settings:
        logger.warning("Нет записи, что существует администратор.")
        return

    logger.info("Существует запись в БД. Работа продолжена")

    type_regime = all_settings[0][0]   # Down / Up
    count_one_gift = all_settings[0][1] # сколько нужно купить каждого
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

    # Фильтруем подарки по диапазону цен
    all_gifts = [(gift_id, values) for gift_id, values in all_premium_gift.items()
                 if price_min <= values[0] <= price_max]

    if not all_gifts:
        logger.warning("Нет подарков в заданном диапазоне цен.")
        return

    # Сортировка по типу режима
    prices = np.array([gift[1][0] for gift in all_gifts])
    remaining_counts = np.array([gift[1][2] if gift[1][2] is not None else np.inf for gift in all_gifts])

    if type_regime == "Down":
        sorted_indices = np.lexsort((remaining_counts, -prices))  # от дорогих к дешёвым
    else:
        sorted_indices = np.lexsort((remaining_counts, prices))   # от дешёвых к дорогим

    sorted_gifts = [all_gifts[i] for i in sorted_indices]

    logger.info(f"Активирован режим: {type_regime}")
    logger.info(f"Начальный баланс бота: {bot_balance} звёзд")

    for gift in sorted_gifts:
        gift_id = gift[0]
        price = gift[1][0]
        total_count = gift[1][1]
        remaining_count = gift[1][2]

        logger.info(f"[{type_regime}] Проверяется подарок ID {gift_id}, цена: {price}, осталось: {remaining_count}")

        bought = 0  # Сколько куплено этого подарка
        while bought < count_one_gift:
            next_balance = bot_balance - price
            if next_balance >= 0:
                bot_balance = next_balance
                try:
                    id_message = await bot.send_gift(
                        gift_id=gift_id,
                        chat_id=int(channel_for_answer),
                        text=comment_for_gift
                    )
                    all_tmp_message.append(id_message)
                    bought += 1
                    logger.info(f"Куплен подарок ID {gift_id}, №{bought}/{count_one_gift}, "
                                f"новый баланс: {bot_balance}")
                except Exception as e:
                    logger.error(f"Ошибка при покупке подарка {gift_id}: {e}")
                    break
            else:
                logger.info(f"Недостаточно звёзд на подарок {gift_id} за {price}. "
                            f"Осталось {bot_balance}. Переход к следующему подарку.")
                break  # Переходим к следующему подарку

    logger.info(f"Финальный баланс: {bot_balance} звёзд")
