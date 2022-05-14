from pickle import NONE
import bot
import discord
import dotenv
import os
import platform
import subprocess

class Seanren(bot.Bot):

    def __init__(self) -> None:
        super().__init__("Seanren", [1, 1], "S")
        self.log.get_logger(self.name).info("I start.")

    async def on_message(self, discord_message : discord.Message) -> None:
        message : bot.Message = bot.Message(self, discord_message)

        if message.parse() != bot.TokenType.TOKEN_ERROR or discord_message.author == self.user:
            await message.command()
            return
        self.log.get_logger(self.name).error(f"This message not understand {message.content}")
        await discord_message.channel.send("This is not a valid message", reference = discord_message)

if __name__ == "__main__":
    dotenv.load_dotenv()
    seanren = Seanren()

    process = None
    if seanren.args.run:
        if platform.system() == "Windows":
            process = subprocess.Popen(["py", "-3", "Ciaham.py"], shell = False)
            seanren.log.get_logger(seanren.name).info("Ciaham is running")
        elif platform.system() == "Linux":
            process = subprocess.Popen(["python3", "Ciaham.py"], shell=True)
            seanren.log.get_logger(seanren.name).info("Ciaham is running")
        else:
            seanren.log.get_logger(seanren.name).error(f"os not supported : {platform.system()}")

    try:
        seanren.run(os.getenv("seanren"))
    except Exception:
        pass
    finally:
        if process is not None:
            process.terminate()
