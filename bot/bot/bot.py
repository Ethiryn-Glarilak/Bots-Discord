import discord
import os
from bot.parser.constructor import ParserMode
from bot.logger.logger import Manager

class Bot(discord.Client):

    def __init__(self, name : str, version : list[int], prefix : str = "0"):
        super().__init__()
        self.command = None
        self.log : Manager = Manager().set_level(int(os.getenv("level")))
        self.name : str = name
        self.mode : ParserMode = ParserMode()
        self.prefix : str = prefix
        self.version : list[int] = version
        self.set_version()

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

    def set_version(self):
        with open("version") as file:
            self.version.append(int(file.read()))
