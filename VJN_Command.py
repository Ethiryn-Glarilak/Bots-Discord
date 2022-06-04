import bot
import discord
import dotenv
import os

class VJN_Command(bot.Bot):

    def __init__(self) -> None:
        super().__init__("VJN_Command", [3, 5], "VJN")
        self.log.get_logger(self.name).info("I start.")

    async def on_ready(self) -> None:
        await self.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(name="🧑‍🍳 Fait des crêpes ! 👩‍🍳"))
        print(self)
        print("Salut tout le monde !")

if __name__ == "__main__":
    dotenv.load_dotenv()
    vjn_command = VJN_Command()
    vjn_command.run(os.getenv("vjn_command"))
