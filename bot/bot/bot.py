import discord

class Bot(discord.Client):

    def __init__(self, name : str, version : list[int]):
        super().__init__()
        self.name = name
        self.version = version
        self.command = None

    def __str__(self) -> str:
        return f"{self.name} ({self.version[0]}.{self.version[1]}.{self.version[2]})"

    async def on_ready(self) -> None:
        await self.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name="Auto-programmer"))
        print(self)
        print("Salut tout le monde !")
