import discord
import os
from bot.parser.constructor import ParserMode
from bot.logger.logger import Manager

class Bot(discord.Client):

    def __init__(self, name : str, version : list[int], prefix : str = "0"):
        super().__init__()
        self.command = None
        self.log = Manager().setLevel(int(os.getenv("level")))
        self.name = name
        self.mode = ParserMode()
        self.prefix = prefix
        self.version = version

    def __str__(self) -> str:
        return f"{self.name} ({self.version[0]}.{self.version[1]}.{self.version[2]})"

    async def on_ready(self) -> None:
        await self.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name="Auto-programmer"))
        print(self)
        print("Salut tout le monde !")

    def __getattribute__(self, __name):
        if __name == "mode":
            return super().__getattribute__("mode")(self.prefix)
        return super().__getattribute__(__name)
