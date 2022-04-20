import discord
import bot
import dotenv
import os

class Seanren(bot.Bot):
    def __init__(self) -> None:
        super().__init__("Seanren", [0, 3, 0])
        self.command = bot.CommandBot.Seanren

    async def on_message(self, discord_message : discord.Message) -> None:
        message : bot.Message = bot.Message(discord_message, self)

        # bot.Message choisit le parser selon les metadata du message
        if message.parse() == bot.TokenType.TOKEN_ERROR and discord_message.author != self.user:
            await discord_message.channel.send("This is not a valid message")
            return
        await message.command()

if __name__ == "__main__":
    dotenv.load_dotenv()
    seanren = Seanren()
    seanren.run(os.getenv("seanren"))
