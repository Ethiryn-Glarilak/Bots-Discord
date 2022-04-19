import discord
import discord_bot
import discord.ext.commands
import dotenv
import os

class Seanren(discord.Client):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Seanren"
        self.version = [0, 2, 0]

    def __str__(self) -> str:
        return f"{self.name} ({self.version[0]}.{self.version[1]}.{self.version[2]})"

    async def on_ready(self) -> None:
        await self.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name="Auto-programmer"))
        print(self)
        print("Salut tout le monde !")

    async def example(self, message : discord.Message):
        await message.channel.send("Coucou")

    async def on_message(self, message : discord.Message) -> None:
        # self.command(discord_bot.Message(message))
        if message.author != self.user:
            await self.example(message)

    def check_message(self, message : discord_bot.Message, level : int = 0) -> bool:
        pass

    async def test(self) -> None:
        await self.channel.send(str(self))

    async def test(self) -> None:
        await self.channel.send("Send")

    async def close(self) -> None:
        await self.close()

    async def reboot(self) -> None:
        try:
            await self.close()
        except Exception:
            print("Exception")
        finally:
            os.system("py -3 Seanren.py")

    async def clear(self, number: int) -> None:
        await self.channel.purge(limit = number + 1)

if __name__ == "__main__":
    dotenv.load_dotenv()
    seanren = Seanren()
    seanren.run(os.getenv("seanren"))
