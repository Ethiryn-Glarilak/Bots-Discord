import argparse
import discord
import discord_components
import os
from bot.bot.import_option import Import
from bot.command.command import Command
from bot.composant.message import Message
from bot.data.postgres import DataBase
from bot.interaction.response import Response
from bot.logger import Manager
from bot.parser.mode import Mode
from extension.module import *

class Bot(discord.Client):

    def __init__(self, name : str, version : list[int], prefix : str = "0"):
        super().__init__(intents = discord.Intents.all())
        self.name : str = name
        self.version : list[int] = version
        self.set_version()
        self.parse_args()
        self.log : Manager = Manager().set_level(int(os.getenv("level")))
        self.mode : Mode = Mode()
        self.prefix : str = prefix
        self.components : discord_components.DiscordComponents = discord_components.DiscordComponents(self)
        self.command : Command = Command()
        self.interaction : Response = Response()
        self.database : dict[DataBase] = {"default" : DataBase(self)}
        Import.load(self, self.args.option)

    def parse_args(self):
        parser = argparse.ArgumentParser(f"{self.name.lower()}.py")
        parser.add_argument(
            "-o",
            "--option",
            dest = "option",
            type = str,
            required=False,
            help = "Optional argument to add other mode to the bot",
            nargs = "+",
        )
        parser.add_argument(
            "--run",
            action='store_true',
            dest = "run",
            required=False,
            help = "Optional argument to run Ciaham",
        )
        parser.add_argument(
            "-e",
            "--environment",
            dest = "environment",
            type = str,
            required=False,
            help = "Optional argument to load specified environment",
        )
        parser.add_argument(
            "-t",
            "--test",
            action='store_true',
            dest = "test",
            required=False,
            help = "Optional argument to use database test",
        )
        self.args = parser.parse_args()
        if self.args.option is None:
            self.args.option = [self.name, "normal"]
        else:
            self.args.option.append(self.name)
            self.args.option.append("normal")

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

    async def on_message(self, discord_message : discord.Message) -> None:
        message : Message = Message(self, discord_message)

        if message.parse() != TokenType.TOKEN_ERROR:
            await message.command()
            return
        self.log.get_logger(self.name).error(f"This message not understand {message.content}")
        await discord_message.channel.send("This is not a valid message", reference = discord_message)

    async def on_button_click(self, interaction : discord_components.interaction) -> None:
        await self.interaction(interaction)

    async def on_select_option(self, interaction : discord_components.interaction) -> None:
        await self.interaction(interaction)
