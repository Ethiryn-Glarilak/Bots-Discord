import discord

async def start(bot):
    await bot.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name="🧑‍🍳 Fait des crêpes ! 👩‍🍳"))
    print(bot)
    print("Salut tout le monde !")

class ReadyVJNCommand:
    additional_function = {
        "start" : start,
    }
