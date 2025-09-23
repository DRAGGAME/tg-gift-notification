import asyncio
import re
import numpy as np
from aiogram.types import Gifts, Gift, Sticker, PhotoSize

from config import bot
from database.db import Sqlbase
from database.other_operations import OtherOperation
from logger import logger

async def start_cmd(pool_sqlbase: Sqlbase, all_tmp_message: list=[]):
    await pool_sqlbase.connect()

    result: Gifts = await bot.get_available_gifts()

    all_premium_gift = {}
    test = [Gift(id='5170145012310081615', sticker=Sticker(file_id='CAACAgIAAxUAAWjO9LHQq1zS51bgLBvEZogAAXZQsAACfBsAApKE2Ev4rcRczyKZtTYE', file_unique_id='AgADfBsAApKE2Es', type='custom_emoji', width=512, height=512, is_animated=True, is_video=False, thumbnail=PhotoSize(file_id='AAMCAgADFQABaM70sdCrXNLnVuAsG8RmiAABdlCwAAJ8GwACkoTYS_itxFzPIpm1AQAHbQADNgQ', file_unique_id='AQADfBsAApKE2Ety', width=128, height=128, file_size=6244), emoji='💝', set_name=None, premium_animation=None, mask_position=None, custom_emoji_id='5465263910414195580', needs_repainting=None, file_size=25528, thumb={'file_id': 'AAMCAgADFQABaM70sdCrXNLnVuAsG8RmiAABdlCwAAJ8GwACkoTYS_itxFzPIpm1AQAHbQADNgQ', 'file_unique_id': 'AQADfBsAApKE2Ety', 'file_size': 6244, 'width': 128, 'height': 128}), star_count=15, upgrade_star_count=None, total_count=20, remaining_count=30, publisher_chat=None), Gift(id='5170233102089322756', sticker=Sticker(file_id='CAACAgIAAxUAAWjO9LGGjNld7kh4uNaxrgABZ5BqtQACrVQAApo_6Up7z5A0L_7IrzYE', file_unique_id='AgADrVQAApo_6Uo', type='custom_emoji', width=512, height=512, is_animated=True, is_video=False, thumbnail=PhotoSize(file_id='AAMCAgADFQABaM70sYaM2V3uSHi41rGuAAFnkGq1AAKtVAACmj_pSnvPkDQv_sivAQAHbQADNgQ', file_unique_id='AQADrVQAApo_6Upy', width=128, height=128, file_size=5282), emoji='🧸', set_name=None, premium_animation=None, mask_position=None, custom_emoji_id='5397915559037785261', needs_repainting=None, file_size=51240, thumb={'file_id': 'AAMCAgADFQABaM70sYaM2V3uSHi41rGuAAFnkGq1AAKtVAACmj_pSnvPkDQv_sivAQAHbQADNgQ', 'file_unique_id': 'AQADrVQAApo_6Upy', 'file_size': 5282, 'width': 128, 'height': 128}), star_count=15, upgrade_star_count=None, total_count=20, remaining_count=10, publisher_chat=None), Gift(id='5170250947678437525', sticker=Sticker(file_id='CAACAgIAAxUAAWjO9LFJB___kBBgObPsPKCsjfwqAAKNSAACsU84SMuB4ge7V_wGNgQ', file_unique_id='AgADjUgAArFPOEg', type='custom_emoji', width=512, height=512, is_animated=True, is_video=False, thumbnail=PhotoSize(file_id='AAMCAgADFQABaM70sUkH__-QEGA5s-w8oKyN_CoAAo1IAAKxTzhIy4HiB7tX_AYBAAdtAAM2BA', file_unique_id='AQADjUgAArFPOEhy', width=128, height=128, file_size=5010), emoji='🎁', set_name=None, premium_animation=None, mask_position=None, custom_emoji_id='5203996991054432397', needs_repainting=None, file_size=10199, thumb={'file_id': 'AAMCAgADFQABaM70sUkH__-QEGA5s-w8oKyN_CoAAo1IAAKxTzhIy4HiB7tX_AYBAAdtAAM2BA', 'file_unique_id': 'AQADjUgAArFPOEhy', 'file_size': 5010, 'width': 128, 'height': 128}), star_count=25, upgrade_star_count=None, total_count=204, remaining_count=50, publisher_chat=None), Gift(id='5168103777563050263', sticker=Sticker(file_id='CAACAgIAAxUAAWjO9LENng3oIpzFJgSs2yibzUxtAAJxGQAC1P-BS9CYmaAv74KENgQ', file_unique_id='AgADcRkAAtT_gUs', type='custom_emoji', width=512, height=512, is_animated=True, is_video=False, thumbnail=PhotoSize(file_id='AAMCAgADFQABaM70sQ2eDeginMUmBKzbKJvNTG0AAnEZAALU_4FL0JiZoC_vgoQBAAdtAAM2BA', file_unique_id='AQADcRkAAtT_gUty', width=128, height=128, file_size=4052), emoji='🌹', set_name=None, premium_animation=None, mask_position=None, custom_emoji_id='5440911110838425969', needs_repainting=None, file_size=48324, thumb={'file_id': 'AAMCAgADFQABaM70sQ2eDeginMUmBKzbKJvNTG0AAnEZAALU_4FL0JiZoC_vgoQBAAdtAAM2BA', 'file_unique_id': 'AQADcRkAAtT_gUty', 'file_size': 4052, 'width': 128, 'height': 128}), star_count=25, upgrade_star_count=None, total_count=204, remaining_count=503, publisher_chat=None), Gift(id='5170144170496491616', sticker=Sticker(file_id='CAACAgIAAxUAAWjO9LGx-eF5JqJINnaCW2b7_HeOAAKBGAAClZ-JSmrGT5kBZFDGNgQ', file_unique_id='AgADgRgAApWfiUo', type='custom_emoji', width=512, height=512, is_animated=True, is_video=False, thumbnail=PhotoSize(file_id='AAMCAgADFQABaM70sbH54Xkmokg2doJbZvv8d44AAoEYAAKVn4lKasZPmQFkUMYBAAdtAAM2BA', file_unique_id='AQADgRgAApWfiUpy', width=128, height=128, file_size=5168), emoji='🎂', set_name=None, premium_animation=None, mask_position=None, custom_emoji_id='5370999492914976897', needs_repainting=None, file_size=19679, thumb={'file_id': 'AAMCAgADFQABaM70sbH54Xkmokg2doJbZvv8d44AAoEYAAKVn4lKasZPmQFkUMYBAAdtAAM2BA', 'file_unique_id': 'AQADgRgAApWfiUpy', 'file_size': 5168, 'width': 128, 'height': 128}), star_count=50, upgrade_star_count=None, total_count=None, remaining_count=None, publisher_chat=None), Gift(id='5170314324215857265', sticker=Sticker(file_id='CAACAgIAAxUAAWjO9LFWILzg_kPWim939GrWqqtBAALeJQACRSDgSsjmE6AUz0NeNgQ', file_unique_id='AgAD3iUAAkUg4Eo', type='custom_emoji', width=512, height=512, is_animated=True, is_video=False, thumbnail=PhotoSize(file_id='AAMCAgADFQABaM70sVYgvOD-Q9aKb3f0ataqq0EAAt4lAAJFIOBKyOYToBTPQ14BAAdtAAM2BA', file_unique_id='AQAD3iUAAkUg4Epy', width=128, height=128, file_size=6932), emoji='💐', set_name=None, premium_animation=None, mask_position=None, custom_emoji_id='5395347834314696158', needs_repainting=None, file_size=48433, thumb={'file_id': 'AAMCAgADFQABaM70sVYgvOD-Q9aKb3f0ataqq0EAAt4lAAJFIOBKyOYToBTPQ14BAAdtAAM2BA', 'file_unique_id': 'AQAD3iUAAkUg4Epy', 'file_size': 6932, 'width': 128, 'height': 128}), star_count=50, upgrade_star_count=None, total_count=None, remaining_count=None, publisher_chat=None), Gift(id='5170564780938756245', sticker=Sticker(file_id='CAACAgIAAxUAAWjO9LHLJ3exdyDc6uY5ck7WoYzfAALLGwAC14mRSzvrMNfF90DPNgQ', file_unique_id='AgADyxsAAteJkUs', type='custom_emoji', width=512, height=512, is_animated=True, is_video=False, thumbnail=PhotoSize(file_id='AAMCAgADFQABaM70scsnd7F3INzq5jlyTtahjN8AAssbAALXiZFLO-sw18X3QM8BAAdtAAM2BA', file_unique_id='AQADyxsAAteJkUty', width=128, height=128, file_size=5538), emoji='🚀', set_name=None, premium_animation=None, mask_position=None, custom_emoji_id='5445284980978621387', needs_repainting=None, file_size=55268, thumb={'file_id': 'AAMCAgADFQABaM70scsnd7F3INzq5jlyTtahjN8AAssbAALXiZFLO-sw18X3QM8BAAdtAAM2BA', 'file_unique_id': 'AQADyxsAAteJkUty', 'file_size': 5538, 'width': 128, 'height': 128}), star_count=50, upgrade_star_count=None, total_count=None, remaining_count=None, publisher_chat=None), Gift(id='5168043875654172773', sticker=Sticker(file_id='CAACAgIAAxUAAWjO9LFRycSufpMg7Wezvwl1SKBsAAKZGwACzagQS38R6izkF899NgQ', file_unique_id='AgADmRsAAs2oEEs', type='custom_emoji', width=512, height=512, is_animated=True, is_video=False, thumbnail=PhotoSize(file_id='AAMCAgADFQABaM70sVHJxK5-kyDtZ7O_CXVIoGwAApkbAALNqBBLfxHqLOQXz30BAAdtAAM2BA', file_unique_id='AQADmRsAAs2oEEty', width=128, height=128, file_size=4546), emoji='🏆', set_name=None, premium_animation=None, mask_position=None, custom_emoji_id='5409008750893734809', needs_repainting=None, file_size=60319, thumb={'file_id': 'AAMCAgADFQABaM70sVHJxK5-kyDtZ7O_CXVIoGwAApkbAALNqBBLfxHqLOQXz30BAAdtAAM2BA', 'file_unique_id': 'AQADmRsAAs2oEEty', 'file_size': 4546, 'width': 128, 'height': 128}), star_count=100, upgrade_star_count=None, total_count=None, remaining_count=None, publisher_chat=None), Gift(id='5170690322832818290', sticker=Sticker(file_id='CAACAgIAAxUAAWjO9LEbmuP7NQVVRqtqUvFc-HaJAALoTwACJx74Ss1NNn7ovmieNgQ', file_unique_id='AgAD6E8AAice-Eo', type='custom_emoji', width=512, height=512, is_animated=True, is_video=False, thumbnail=PhotoSize(file_id='AAMCAgADFQABaM70sRua4_s1BVVGq2pS8Vz4dokAAuhPAAInHvhKzU02fui-aJ4BAAdtAAM2BA', file_unique_id='AQAD6E8AAice-Epy', width=128, height=128, file_size=4672), emoji='💍', set_name=None, premium_animation=None, mask_position=None, custom_emoji_id='5402100905883488232', needs_repainting=None, file_size=61230, thumb={'file_id': 'AAMCAgADFQABaM70sRua4_s1BVVGq2pS8Vz4dokAAuhPAAInHvhKzU02fui-aJ4BAAdtAAM2BA', 'file_unique_id': 'AQAD6E8AAice-Epy', 'file_size': 4672, 'width': 128, 'height': 128}), star_count=100, upgrade_star_count=None, total_count=None, remaining_count=None, publisher_chat=None), Gift(id='5170521118301225164', sticker=Sticker(file_id='CAACAgIAAxUAAWjO9LEBeD8YhV3Zm2iqis7h-sVoAAIbHgACQEjwS6XKX-OK2k1MNgQ', file_unique_id='AgADGx4AAkBI8Es', type='custom_emoji', width=512, height=512, is_animated=True, is_video=False, thumbnail=PhotoSize(file_id='AAMCAgADFQABaM70sQF4PxiFXdmbaKqKzuH6xWgAAhseAAJASPBLpcpf44raTUwBAAdtAAM2BA', file_unique_id='AQADGx4AAkBI8Ety', width=128, height=128, file_size=3784), emoji='💎', set_name=None, premium_animation=None, mask_position=None, custom_emoji_id='5471952986970267163', needs_repainting=None, file_size=47932, thumb={'file_id': 'AAMCAgADFQABaM70sQF4PxiFXdmbaKqKzuH6xWgAAhseAAJASPBLpcpf44raTUwBAAdtAAM2BA', 'file_unique_id': 'AQADGx4AAkBI8Ety', 'file_size': 3784, 'width': 128, 'height': 128}), star_count=100, upgrade_star_count=None, total_count=None, remaining_count=None, publisher_chat=None), Gift(id='6028601630662853006', sticker=Sticker(file_id='CAACAgIAAxUAAWjO9LGPMhw3dnGDePw_tN6B3Rf1AALXGAACy0WJSqKYQ7cuIwaJNgQ', file_unique_id='AgAD1xgAAstFiUo', type='custom_emoji', width=512, height=512, is_animated=True, is_video=False, thumbnail=PhotoSize(file_id='AAMCAgADFQABaM70sY8yHDd2cYN4_D-03oHdF_UAAtcYAALLRYlKophDty4jBokBAAdtAAM2BA', file_unique_id='AQAD1xgAAstFiUpy', width=128, height=128, file_size=3542), emoji='🍾', set_name=None, premium_animation=None, mask_position=None, custom_emoji_id='5370900768796711127', needs_repainting=None, file_size=42245, thumb={'file_id': 'AAMCAgADFQABaM70sY8yHDd2cYN4_D-03oHdF_UAAtcYAALLRYlKophDty4jBokBAAdtAAM2BA', 'file_unique_id': 'AQAD1xgAAstFiUpy', 'file_size': 3542, 'width': 128, 'height': 128}), star_count=50, upgrade_star_count=None, total_count=None, remaining_count=None, publisher_chat=None)]
    logger.info("Проверка на подарки")
    for info_a_gift in test:
        if hasattr(info_a_gift, "total_count"):
            total_count = getattr(info_a_gift, "total_count")

            if total_count is not None:
                end_count = getattr(info_a_gift, "remaining_count")
                price_gift = getattr(info_a_gift, "star_count")
                gift_id = getattr(info_a_gift, "id")
                logger.info("Существует подарок премиум-подарок")
                all_premium_gift[gift_id] = (price_gift, total_count, end_count, )

    all_settings = await pool_sqlbase.execute_query("""SELECT type_regime, count_gifts, count_one_gift, price_min, 
                                                              price_max, bot_balance, default_channel, admin_chat_id 
                                                       FROM settings_table WHERE admin_chat_id <> 'default'""")
    if not all_settings:
        logger.warning("Нет записи, что существует администратор. ")
        return

    logger.info("Существует запись в БД. Работа продолжена")

    type_regime = all_settings[0][0]
    count_gifts = all_settings[0][1]
    count_one_gift = all_settings[0][2]
    price_min = all_settings[0][3]
    price_max = all_settings[0][4]
    bot_balance = all_settings[0][5]
    default_channel = all_settings[0][6]
    admin_chat_id = all_settings[0][7]

    if type_regime == "down":
        logger.info("Активирован режим покупки с высшего до нисшего...")
        all_gifts = [(gift_id, values) for gift_id, values in all_premium_gift.items()
                     if price_min <= values[0] <= price_max]

        if all_gifts:
            logger.info("Доп. проверка на подарки, пройдена")
            prices = np.array([gift[1][0] for gift in all_gifts])
            remaining_counts = np.array([gift[1][2] if gift[1][2] is not None else np.inf for gift in all_gifts])

            sorted_indices = np.lexsort((remaining_counts, -prices))
            sorted_gifts = [all_gifts[i] for i in sorted_indices]

            for gift in sorted_gifts:
                gift_id = gift[0]
                price = gift[1][0]
                total_count = gift[1][1]
                remaining_count = gift[1][2]
                logger.info(f"ID: {gift_id}, Цена (звёзды): {price}, Total: {total_count}, Осталось: {remaining_count}")

            for gift in sorted_gifts:
                gift_id = gift[0]
                gift_price = gift[1][0]

                for _ in range(count_one_gift):
                    if bot_balance - gift_price >= 0:

                        bot_balance -= gift_price
                        id_message = await bot.send_gift(gift_id=gift_id, chat_id=default_channel)
                        all_tmp_message.append(id_message)
                        await asyncio.sleep(10)

                    else:
                        logger.info(f"Бот не может купить подарок. \nХватает ли баланса: {bool(bot_balance-gift_price)}")
                        await bot.send_message(chat_id=admin_chat_id, text="У бота кончились звёзды")
            for tmp_message in all_tmp_message:
                await bot.delete_message(chat_id=tmp_message.chat.id, message_id=tmp_message.message_id)
                await asyncio.sleep(10)


# sqlbase = OtherOperation()
# asyncio.run(start_cmd(pool_sqlbase=sqlbase))

