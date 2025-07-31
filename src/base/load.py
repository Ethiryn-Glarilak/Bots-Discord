import discord
import os

from discord.ext import commands
from src.bot import Bot

class Base(commands.Cog):
    """Base class for the bot's load extension."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @discord.app_commands.command()
    async def reboot(self, interaction: discord.Interaction):
        """Reboot the bot."""
        if await self.bot.is_owner(interaction.user):
            await interaction.response.send_message("Rebooting the bot...", ephemeral=True)
            channel = self.bot.get_channel(int(os.getenv("LOG_CHANNEL_ID", "0")))
            if type(channel) is discord.TextChannel:
                await channel.send(f"Command reboot of {self.bot.name}.")

            def get_args(self) -> str:
                # result = "".join(f"{str(args)} " for args in self.bot.args.option if self.bot.name != args != "normal")
                # if result != '':
                #     result = f"-o {result}"
                # if self.bot.args.run:
                #     result += "--run"
                # return result
                return ""

            try:
                ## Attention mauvaise coupure de la db
                await self.bot.close()
            except Exception:
                self.bot.log("command").error("Failed to close the bot gracefully.")
            finally:
                # vérifie si le script à été lancé avec python ou uv
                # if platform.system() == "Windows":
                #    os.system(f"py -3 {self.bot.name}.py {get_args(self)}")
                # elif platform.system() == "Linux":
                    os.system(f"uv run {self.bot.name}.py {get_args(self)}")
                #     os.system(f"python3 {self.bot.name}.py {get_args(self)}")
                # else:
                #     self.bot.log("command").error(f"os not supported : {platform.system()}")

        else:
            await interaction.response.send_message("You do not have permission to reboot the bot.", ephemeral=True)


async def setup(bot: Bot):
    """Setup function to add the base load cog to the bot."""
    bot.log(name="base.load").info("Loading base load extension...")
    await bot.add_cog(Base(bot))
    bot.log(name="base.load").info("Base load extension loaded successfully.")
