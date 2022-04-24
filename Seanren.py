import bot
import discord
import dotenv
import os

class Seanren(bot.Bot):

    def __init__(self) -> None:
        super().__init__("Seanren", [1, 1], "S")
        self.command = bot.CommandBot.Seanren
        self.log.get_logger(self.name).info("I start.")

    async def on_message(self, discord_message : discord.Message) -> None:
        message : bot.Message = bot.Message(discord_message, self)

        if message.parse() != bot.TokenType.TOKEN_ERROR or discord_message.author == self.user:
            await message.command()
            return
        self.log.get_logger(self.name).error(f"This message not understand {message.message.content}")
        await discord_message.channel.send("This is not a valid message", reference = discord_message)

if __name__ == "__main__":
    dotenv.load_dotenv()
    seanren = Seanren()
    seanren.run(os.getenv("seanren"))
