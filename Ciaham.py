import bot
import discord
import dotenv
import os

class Ciaham(bot.Bot):

    def __init__(self) -> None:
        super().__init__("Ciaham", [0, 1, 0], "C")
        self.command = bot.CommandBot.Ciaham
        self.log.getLogger(name = self.name).start(level = int(os.getenv("level"))).info("I start.")

    async def on_message(self, discord_message : discord.Message) -> None:
        message : bot.Message = bot.Message(discord_message, self)

        if message.parse() == bot.TokenType.TOKEN_ERROR and discord_message.author != self.user:
            await discord_message.channel.send("This is not a valid message", reference = discord_message)
            return
        await message.command()

if __name__ == "__main__":
    dotenv.load_dotenv()
    ciaham = Ciaham()
    ciaham.run(os.getenv("ciaham"))
