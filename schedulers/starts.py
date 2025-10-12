import asyncio
import re
import numpy as np
from aiogram.types import Gifts, Gift, Sticker, PhotoSize

from config import bot
from database.admin_operations import AdminOperations
from database.db import Sqlbase
from database.other_operations import OtherOperation
from functions.get_bot_stars import get_bot_stars
from logger import logger

async def start_cmd(pool_sqlbase: AdminOperations, all_tmp_message: list=[]):

    result: Gifts = await bot.get_available_gifts()
    print(result)
    all_premium_gift = {}
    gifts = [Gift(id='5170145012310081615',
                  sticker=Sticker(file_id='CAACAgIAAxUAAWjrfGQvfm3FiGLqKoRbSna6mhJtAAJ8GwACkoTYS_itxFzPIpm1NgQ',
                                  file_unique_id='AgADfBsAApKE2Es', type='custom_emoji', width=512, height=512,
                                  is_animated=True, is_video=False, thumbnail=PhotoSize(
                          file_id='AAMCAgADFQABaOt8ZC9-bcWIYuoqhFtKdrqaEm0AAnwbAAKShNhL-K3EXM8imbUBAAdtAAM2BA',
                          file_unique_id='AQADfBsAApKE2Ety', width=128, height=128, file_size=6244), emoji='💝',
                                  set_name=None, premium_animation=None, mask_position=None,
                                  custom_emoji_id='5465263910414195580', needs_repainting=None, file_size=25528, thumb={
                          'file_id': 'AAMCAgADFQABaOt8ZC9-bcWIYuoqhFtKdrqaEm0AAnwbAAKShNhL-K3EXM8imbUBAAdtAAM2BA',
                          'file_unique_id': 'AQADfBsAApKE2Ety', 'file_size': 6244, 'width': 128, 'height': 128}),
                  star_count=15, upgrade_star_count=None, total_count=0, remaining_count=None, publisher_chat=None),
             Gift(id='5170233102089322756',
                  sticker=Sticker(file_id='CAACAgIAAxUAAWjrfGQgjYABVUhzhDtVmedBmduOAAKtVAACmj_pSnvPkDQv_sivNgQ',
                                  file_unique_id='AgADrVQAApo_6Uo', type='custom_emoji', width=512, height=512,
                                  is_animated=True, is_video=False, thumbnail=PhotoSize(
                          file_id='AAMCAgADFQABaOt8ZCCNgAFVSHOEO1WZ50GZ244AAq1UAAKaP-lKe8-QNC_-yK8BAAdtAAM2BA',
                          file_unique_id='AQADrVQAApo_6Upy', width=128, height=128, file_size=5282), emoji='🧸',
                                  set_name=None, premium_animation=None, mask_position=None,
                                  custom_emoji_id='5397915559037785261', needs_repainting=None, file_size=51240, thumb={
                          'file_id': 'AAMCAgADFQABaOt8ZCCNgAFVSHOEO1WZ50GZ244AAq1UAAKaP-lKe8-QNC_-yK8BAAdtAAM2BA',
                          'file_unique_id': 'AQADrVQAApo_6Upy', 'file_size': 5282, 'width': 128, 'height': 128}),
                  star_count=15, upgrade_star_count=None, total_count=10, remaining_count=1, publisher_chat=None),
             Gift(id='5170250947678437525',
                  sticker=Sticker(file_id='CAACAgIAAxUAAWjrfGSgIIRODNumQc58J0t8h6VcAAKNSAACsU84SMuB4ge7V_wGNgQ',
                                  file_unique_id='AgADjUgAArFPOEg', type='custom_emoji', width=512, height=512,
                                  is_animated=True, is_video=False, thumbnail=PhotoSize(
                          file_id='AAMCAgADFQABaOt8ZKAghE4M26ZBznwnS3yHpVwAAo1IAAKxTzhIy4HiB7tX_AYBAAdtAAM2BA',
                          file_unique_id='AQADjUgAArFPOEhy', width=128, height=128, file_size=5010), emoji='🎁',
                                  set_name=None, premium_animation=None, mask_position=None,
                                  custom_emoji_id='5203996991054432397', needs_repainting=None, file_size=10199, thumb={
                          'file_id': 'AAMCAgADFQABaOt8ZKAghE4M26ZBznwnS3yHpVwAAo1IAAKxTzhIy4HiB7tX_AYBAAdtAAM2BA',
                          'file_unique_id': 'AQADjUgAArFPOEhy', 'file_size': 5010, 'width': 128, 'height': 128}),
                  star_count=25, upgrade_star_count=None, total_count=40, remaining_count=1, publisher_chat=None),
             Gift(id='5168103777563050263',
                  sticker=Sticker(file_id='CAACAgIAAxUAAWjrfGQaMzuT5xFltvDmnbisx1FjAAJxGQAC1P-BS9CYmaAv74KENgQ',
                                  file_unique_id='AgADcRkAAtT_gUs', type='custom_emoji', width=512, height=512,
                                  is_animated=True, is_video=False, thumbnail=PhotoSize(
                          file_id='AAMCAgADFQABaOt8ZBozO5PnEWW28OaduKzHUWMAAnEZAALU_4FL0JiZoC_vgoQBAAdtAAM2BA',
                          file_unique_id='AQADcRkAAtT_gUty', width=128, height=128, file_size=4052), emoji='🌹',
                                  set_name=None, premium_animation=None, mask_position=None,
                                  custom_emoji_id='5440911110838425969', needs_repainting=None, file_size=48324, thumb={
                          'file_id': 'AAMCAgADFQABaOt8ZBozO5PnEWW28OaduKzHUWMAAnEZAALU_4FL0JiZoC_vgoQBAAdtAAM2BA',
                          'file_unique_id': 'AQADcRkAAtT_gUty', 'file_size': 4052, 'width': 128, 'height': 128}),
                  star_count=25, upgrade_star_count=None, total_count=39, remaining_count=13, publisher_chat=None),
             Gift(id='5170144170496491616',
                  sticker=Sticker(file_id='CAACAgIAAxUAAWjrfGTQlipMwpHrbuMtRsNGRNpWAAKBGAAClZ-JSmrGT5kBZFDGNgQ',
                                  file_unique_id='AgADgRgAApWfiUo', type='custom_emoji', width=512, height=512,
                                  is_animated=True, is_video=False, thumbnail=PhotoSize(
                          file_id='AAMCAgADFQABaOt8ZNCWKkzCketu4y1Gw0ZE2lYAAoEYAAKVn4lKasZPmQFkUMYBAAdtAAM2BA',
                          file_unique_id='AQADgRgAApWfiUpy', width=128, height=128, file_size=5168), emoji='🎂',
                                  set_name=None, premium_animation=None, mask_position=None,
                                  custom_emoji_id='5370999492914976897', needs_repainting=None, file_size=19679, thumb={
                          'file_id': 'AAMCAgADFQABaOt8ZNCWKkzCketu4y1Gw0ZE2lYAAoEYAAKVn4lKasZPmQFkUMYBAAdtAAM2BA',
                          'file_unique_id': 'AQADgRgAApWfiUpy', 'file_size': 5168, 'width': 128, 'height': 128}),
                  star_count=50, upgrade_star_count=None, total_count=23, remaining_count=0, publisher_chat=None),
             Gift(id='5170314324215857265',
                  sticker=Sticker(file_id='CAACAgIAAxUAAWjrfGR5C3LsaYJmFfvTSu-dsSL1AALeJQACRSDgSsjmE6AUz0NeNgQ',
                                  file_unique_id='AgAD3iUAAkUg4Eo', type='custom_emoji', width=512, height=512,
                                  is_animated=True, is_video=False, thumbnail=PhotoSize(
                          file_id='AAMCAgADFQABaOt8ZHkLcuxpgmYV-9NK752xIvUAAt4lAAJFIOBKyOYToBTPQ14BAAdtAAM2BA',
                          file_unique_id='AQAD3iUAAkUg4Epy', width=128, height=128, file_size=6932), emoji='💐',
                                  set_name=None, premium_animation=None, mask_position=None,
                                  custom_emoji_id='5395347834314696158', needs_repainting=None, file_size=48433, thumb={
                          'file_id': 'AAMCAgADFQABaOt8ZHkLcuxpgmYV-9NK752xIvUAAt4lAAJFIOBKyOYToBTPQ14BAAdtAAM2BA',
                          'file_unique_id': 'AQAD3iUAAkUg4Epy', 'file_size': 6932, 'width': 128, 'height': 128}),
                  star_count=50, upgrade_star_count=None, total_count=12, remaining_count=3, publisher_chat=None),
             Gift(id='5170564780938756245',
                  sticker=Sticker(file_id='CAACAgIAAxUAAWjrfGSbRFsyavJXHqrAu94Vjf3yAALLGwAC14mRSzvrMNfF90DPNgQ',
                                  file_unique_id='AgADyxsAAteJkUs', type='custom_emoji', width=512, height=512,
                                  is_animated=True, is_video=False, thumbnail=PhotoSize(
                          file_id='AAMCAgADFQABaOt8ZJtEWzJq8lceqsC73hWN_fIAAssbAALXiZFLO-sw18X3QM8BAAdtAAM2BA',
                          file_unique_id='AQADyxsAAteJkUty', width=128, height=128, file_size=5538), emoji='🚀',
                                  set_name=None, premium_animation=None, mask_position=None,
                                  custom_emoji_id='5445284980978621387', needs_repainting=None, file_size=55268, thumb={
                          'file_id': 'AAMCAgADFQABaOt8ZJtEWzJq8lceqsC73hWN_fIAAssbAALXiZFLO-sw18X3QM8BAAdtAAM2BA',
                          'file_unique_id': 'AQADyxsAAteJkUty', 'file_size': 5538, 'width': 128, 'height': 128}),
                  star_count=50, upgrade_star_count=None, total_count=0, remaining_count=32, publisher_chat=None),
             Gift(id='5168043875654172773',
                  sticker=Sticker(file_id='CAACAgIAAxUAAWjrfGQOUjcxV0hFlNQGrx-xqlgWAAKZGwACzagQS38R6izkF899NgQ',
                                  file_unique_id='AgADmRsAAs2oEEs', type='custom_emoji', width=512, height=512,
                                  is_animated=True, is_video=False, thumbnail=PhotoSize(
                          file_id='AAMCAgADFQABaOt8ZA5SNzFXSEWU1AavH7GqWBYAApkbAALNqBBLfxHqLOQXz30BAAdtAAM2BA',
                          file_unique_id='AQADmRsAAs2oEEty', width=128, height=128, file_size=4546), emoji='🏆',
                                  set_name=None, premium_animation=None, mask_position=None,
                                  custom_emoji_id='5409008750893734809', needs_repainting=None, file_size=60319, thumb={
                          'file_id': 'AAMCAgADFQABaOt8ZA5SNzFXSEWU1AavH7GqWBYAApkbAALNqBBLfxHqLOQXz30BAAdtAAM2BA',
                          'file_unique_id': 'AQADmRsAAs2oEEty', 'file_size': 4546, 'width': 128, 'height': 128}),
                  star_count=100, upgrade_star_count=None, total_count=111, remaining_count=32, publisher_chat=None),
             Gift(id='5170690322832818290',
                  sticker=Sticker(file_id='CAACAgIAAxUAAWjrfGRzM_mJfo_V-xIblnoEI_hOAALoTwACJx74Ss1NNn7ovmieNgQ',
                                  file_unique_id='AgAD6E8AAice-Eo', type='custom_emoji', width=512, height=512,
                                  is_animated=True, is_video=False, thumbnail=PhotoSize(
                          file_id='AAMCAgADFQABaOt8ZHMz-Yl-j9X7EhuWegQj-E4AAuhPAAInHvhKzU02fui-aJ4BAAdtAAM2BA',
                          file_unique_id='AQAD6E8AAice-Epy', width=128, height=128, file_size=4672), emoji='💍',
                                  set_name=None, premium_animation=None, mask_position=None,
                                  custom_emoji_id='5402100905883488232', needs_repainting=None, file_size=61230, thumb={
                          'file_id': 'AAMCAgADFQABaOt8ZHMz-Yl-j9X7EhuWegQj-E4AAuhPAAInHvhKzU02fui-aJ4BAAdtAAM2BA',
                          'file_unique_id': 'AQAD6E8AAice-Epy', 'file_size': 4672, 'width': 128, 'height': 128}),
                  star_count=100, upgrade_star_count=None, total_count=3, remaining_count=0, publisher_chat=None),
             Gift(id='5170521118301225164',
                  sticker=Sticker(file_id='CAACAgIAAxUAAWjrfGSxmGtIoUNJpzoWG_VcH4cBAAIbHgACQEjwS6XKX-OK2k1MNgQ',
                                  file_unique_id='AgADGx4AAkBI8Es', type='custom_emoji', width=512, height=512,
                                  is_animated=True, is_video=False, thumbnail=PhotoSize(
                          file_id='AAMCAgADFQABaOt8ZLGYa0ihQ0mnOhYb9VwfhwEAAhseAAJASPBLpcpf44raTUwBAAdtAAM2BA',
                          file_unique_id='AQADGx4AAkBI8Ety', width=128, height=128, file_size=3784), emoji='💎',
                                  set_name=None, premium_animation=None, mask_position=None,
                                  custom_emoji_id='5471952986970267163', needs_repainting=None, file_size=47932, thumb={
                          'file_id': 'AAMCAgADFQABaOt8ZLGYa0ihQ0mnOhYb9VwfhwEAAhseAAJASPBLpcpf44raTUwBAAdtAAM2BA',
                          'file_unique_id': 'AQADGx4AAkBI8Ety', 'file_size': 3784, 'width': 128, 'height': 128}),
                  star_count=100, upgrade_star_count=None, total_count=12, remaining_count=390, publisher_chat=None),
             Gift(id='6028601630662853006',
                  sticker=Sticker(file_id='CAACAgIAAxUAAWjrfGQCHnVZJnAbyjeQuTytje1EAALXGAACy0WJSqKYQ7cuIwaJNgQ',
                                  file_unique_id='AgAD1xgAAstFiUo', type='custom_emoji', width=512, height=512,
                                  is_animated=True, is_video=False, thumbnail=PhotoSize(
                          file_id='AAMCAgADFQABaOt8ZAIedVkmcBvKN5C5PK2N7UQAAtcYAALLRYlKophDty4jBokBAAdtAAM2BA',
                          file_unique_id='AQAD1xgAAstFiUpy', width=128, height=128, file_size=3542), emoji='🍾',
                                  set_name=None, premium_animation=None, mask_position=None,
                                  custom_emoji_id='5370900768796711127', needs_repainting=None, file_size=42245, thumb={
                          'file_id': 'AAMCAgADFQABaOt8ZAIedVkmcBvKN5C5PK2N7UQAAtcYAALLRYlKophDty4jBokBAAdtAAM2BA',
                          'file_unique_id': 'AQAD1xgAAstFiUpy', 'file_size': 3542, 'width': 128, 'height': 128}),
                  star_count=50, upgrade_star_count=None, total_count=32, remaining_count=121, publisher_chat=None)]

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