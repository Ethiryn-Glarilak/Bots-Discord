import bot
import discord
import discord_components
import dotenv
import os

class Ciaham(bot.Bot):

    def __init__(self) -> None:
        super().__init__("Ciaham", [1, 1], "C")
        self.log.get_logger(self.name).info("I start.")

    async def on_message(self, discord_message : discord.Message) -> None:
        message : bot.Message = bot.Message(self, discord_message)

        if message.parse() != bot.TokenType.TOKEN_ERROR or discord_message.author == self.user:
            await message.command()
            return
        self.log.getLogger(self.name).error(f"This message not understand {message.content}")
        await discord_message.channel.send("This is not a valid message", reference = discord_message)

    async def on_button_click(self, interaction : discord_components.interaction) -> None:
        await self.interaction(interaction)

    async def on_select_option(self, interaction : discord_components.interaction) -> None:
        await self.interaction(interaction)

if __name__ == "__main__":
    dotenv.load_dotenv()
    ciaham = Ciaham()
    ciaham.run(os.getenv("ciaham"))
