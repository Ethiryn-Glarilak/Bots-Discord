import discord
import os
import pathlib
import src

from discord.ext import commands
from src.logger import LoggerManager

class Bot(commands.Bot, discord.Client):

    def __init__(self, name: str, version: list[int], prefix: str = "0"):
        super().__init__(intents=discord.Intents.all(), command_prefix=prefix, help_command=None)
        self.__name: str = name
        self.__version: list[int] = version
        self.set_version()
        self.parse_args()
        self.__log = LoggerManager().set_level(LoggerManager.str_to_level(os.getenv("log_level", "INFO")))
        self.init_database()

    def parse_args(self):
        """Parse command line arguments."""
        import argparse
        parser = argparse.ArgumentParser(description=f"{self.name} bot arguments")
        parser.add_argument(
            "--run",
            action='store_true',
            dest = "run",
            required=False,
            help = "Optional argument to run Ciaham",
        )
        parser.add_argument(
            "-o",
            "--option",
            action='append',
            dest = "option",
            required=False,
            help = "Optional argument to specify options for the bot, can be used multiple times. Default is the bot name.",
            default=None
        )
        self.args = parser.parse_args()
        if self.args.option is None:
            self.args.option = [self.name]
        else:
            self.args.option.append(self.name)

    @property
    def name(self) -> str:
        """Get the name of the bot."""
        return self.__name

    def database(self, name: str = "default") -> "src.Database":
        """Get the database instance by name."""
        if name not in self.__database:
            self.__database[name] = src.Database(dbname=name)
        return self.__database[name]

    def init_database(self):
        """Initialize the default database."""
        self.__database = {"default": src.Database(logger=self.log(name="database_default"))}

    def log(self, name: str):
        """Log a message with the specified level."""
        return self.__log.get_logger(name)

    async def load_extensions(self):
        """Load all extensions from the extensions directory."""
        self.log(name=self.__name).info("Loading extensions...")
        extensions_dir = pathlib.Path(os.getcwd()) / 'extensions'
        for extension_dir in extensions_dir.iterdir():
            if extension_dir.is_dir():
                if not (extension_dir / 'load.py').exists():
                    self.log(name=self.__name).warning(f"Extension {extension_dir.name} does not have a load.py file, skipping.")
                    continue
                await self.load_extension(f"extensions.{extension_dir.name}.load")
        self.log(name=self.__name).info("All extensions loaded.")

    async def setup_hook(self):
        """Setup hook called when the bot is ready to start."""
        self.log(name=self.__name).info("Setting up bot...")
        await self.load_extension("src.base.load")
        await self.load_extensions()

    def set_version(self):
        with open("version", "r+") as file:
            self.__version.append(int(file.read().strip() or "0"))
            file.seek(0)
            file.write(str(self.__version[-1] + 1))
            file.truncate()

    def __str__(self) -> str:
        return f"{self.__name} ({self.__version[0]}.{self.__version[1]}.{self.__version[2]})"

    async def on_message(self, discord_message: discord.Message) -> None:
        if discord_message.author.bot:
            return
        # await self.process_commands(discord_message)
        self.__log.get_logger(self.__name).error(f"This message not understand {discord_message.content}")

    async def on_ready(self):
        """Called when the bot is ready."""
        await self.tree.sync()
        await self.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name="Auto-programmer"))
        self.__log.get_logger(self.__name).info(f"{self.__name} is ready with version {self.__version[0]}.{self.__version[1]}.{self.__version[2]}")

    async def close(self):
        """Close the bot and clean up resources."""
        self.__log.get_logger(self.__name).info("Closing the bot...")
        await super().close()
        for name, db in self.__database.items():
            db.close()
            self.__log.get_logger(self.__name).info(f"Database {name} closed successfully.")
        self.__log.get_logger(self.__name).info("Bot closed successfully.")
