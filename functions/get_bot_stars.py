from config import bot


async def get_bot_stars():
    bot_balance_stars = await bot.get_my_star_balance(request_timeout=30)

    if hasattr(bot_balance_stars, "amount"):
        bot_balance_stars = getattr(bot_balance_stars, "amount")
        return bot_balance_stars
    else:
        return None