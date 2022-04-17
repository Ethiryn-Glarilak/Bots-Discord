import discord
import discord_bot
import discord.ext.commands
import dotenv
import os

class Seanren(discord.ext.commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix = "")
        self.name = "Seanren"
        self.version = [0, 1, 0]
        self.load_command()

    def __str__(self) -> str:
        return f"{self.name} ({self.version[0]}.{self.version[1]}.{self.version[2]})"

    async def on_ready(self) -> None:
        await self.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name="Auto-programmer"))
        print(self)
        print("Salut tout le monde !")

    def check_message(self, message : discord_bot.Message, level : int = 0) -> bool:
        pass

    def load_command(self) -> None:
        @self.command(name = "version")
        async def test(ctx) -> None:
            await ctx.channel.send(str(self))

        @self.command(name = "t")
        async def test(ctx) -> None:
            await ctx.channel.send("Send")

        @self.command(name = "close")
        async def close(ctx) -> None:
            await self.close()

        @self.command(name = "reboot")
        async def reboot(ctx) -> None:
            try:
                await self.close()
            except Exception:
                print("Exception")
            finally:
                os.system("py -3 Seanren.py")

        @self.command(name = "clear")
        async def clear(ctx, number: int) -> None:
            await ctx.channel.purge(limit = number + 1)

if __name__ == "__main__":
    dotenv.load_dotenv()
    seanren = Seanren()
    seanren.run(os.getenv("seanren"))
