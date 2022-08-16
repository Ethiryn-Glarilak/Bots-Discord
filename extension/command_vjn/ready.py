async def start(bot):
    await bot.vjn_object.start(bot)

class ReadyCommandVJN:
    additional_function = {
        "start" : start,
    }
