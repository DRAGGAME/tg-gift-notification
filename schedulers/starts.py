import numpy as np
from aiogram.types import Gifts

from config import bot
from database.admin_operations import AdminOperations
from functions.get_bot_stars import get_bot_stars
from logger import logger


async def start_cmd(pool_sqlbase: AdminOperations, all_tmp_message: list = []):
    sorted_gifts = []
    gifts: Gifts = await bot.get_available_gifts()
    all_premium_gift = {}

    logger.info("Проверка на подарки")

    if not hasattr(gifts, "gifts") or not gifts.gifts:
        logger.warning("Список подарков пуст или структура неверна.")
        return

    for info_a_gift in gifts.gifts:
        if hasattr(info_a_gift, "total_count"):
            total_count = getattr(info_a_gift, "total_count", None)
            if total_count is not None:
                end_count = getattr(info_a_gift, "remaining_count", None)
                price_gift = getattr(info_a_gift, "star_count", None)
                gift_id = getattr(info_a_gift, "id", None)

                logger.info(f"🎁 Лимитированный подарок найден: ID={gift_id}, цена={price_gift}, всего={total_count}, осталось={end_count}")

                all_premium_gift[gift_id] = (price_gift, total_count, end_count)

    if not all_premium_gift:
        logger.info("Нет лимитированных подарков с total_count.")
        return

    all_settings = await pool_sqlbase.select_profile_last()
    if not all_settings:
        logger.warning("Нет записи, что существует администратор.")
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

    if channel_for_answer == "":
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

    # Сортируем подарки в зависимости от режима
    all_gifts = [(gift_id, values) for gift_id, values in all_premium_gift.items()
                 if price_min <= values[0] <= price_max]

    if not all_gifts:
        logger.warning("Нет подарков в заданном диапазоне цен.")
        return

    prices = np.array([gift[1][0] for gift in all_gifts])
    remaining_counts = np.array([gift[1][2] if gift[1][2] is not None else np.inf for gift in all_gifts])

    if type_regime == "Down":
        sorted_indices = np.lexsort((remaining_counts, -prices))
        logger.info("Активирован режим покупки с высшего до низшего...")
    else:
        sorted_indices = np.lexsort((remaining_counts, prices))
        logger.info("Активирован режим покупки с низшего до высшего...")

    sorted_gifts = [all_gifts[i] for i in sorted_indices]

    # Логируем отсортированные подарки
    for gift in sorted_gifts:
        gift_id = gift[0]
        price = gift[1][0]
        total_count = gift[1][1]
        remaining_count = gift[1][2]
        logger.info(f"ID: {gift_id}, Цена: {price}, Total: {total_count}, Осталось: {remaining_count}")

    # ПОКУПКА: нужно купить count_one_gift штук суммарно, распределяя по подаркам
    gifts_needed = count_one_gift  # сколько осталось купить

    for gift in sorted_gifts:
        if gifts_needed <= 0:
            break  # Всё куплено

        gift_id = gift[0]
        gift_price = gift[1][0]
        gift_remaining = gift[1][2] if gift[1][2] is not None else np.inf

        # Максимум сколько можно купить этого подарка (с учётом остатка)
        max_can_buy = min(gifts_needed, gift_remaining)

        bought_count = 0

        while bought_count < max_can_buy:
            if bot_balance >= gift_price:
                bot_balance -= gift_price
                try:
                    id_message = await bot.send_gift(
                        gift_id=gift_id,
                        chat_id=int(channel_for_answer),
                        text=comment_for_gift
                    )
                    all_tmp_message.append(id_message)
                    bought_count += 1
                    gifts_needed -= 1
                    logger.info(f"Куплен подарок ID {gift_id} ({bought_count}/{max_can_buy}), осталось купить: {gifts_needed}, баланс: {bot_balance}")
                except Exception as e:
                    logger.error(f"Ошибка при покупке подарка {gift_id}: {e}")
                    break
            else:
                logger.info(f"Недостаточно звёзд для покупки подарка ID {gift_id} по цене {gift_price}. Текущий баланс: {bot_balance}")
                break

    if gifts_needed > 0:
        logger.warning(f"Не удалось купить полное количество подарков. Осталось купить: {gifts_needed}")

    logger.info(f"Финальный баланс: {bot_balance}")
