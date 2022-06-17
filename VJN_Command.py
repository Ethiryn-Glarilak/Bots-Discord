import aiohttp
import src
import discord
import dotenv
import os

class VJN_Command(src.Bot):

    def __init__(self) -> None:
        super().__init__("VJN_Command", [3, 5], "VJN")
        self.log.get_logger(self.name).info("I start.")

if __name__ == "__main__":
    dotenv.load_dotenv()
    vjn_command = VJN_Command()
    try:
        vjn_command.run(os.getenv("vjn_command"))
    except aiohttp.ClientConnectionError:
        print("Failed to connect to vjn_command")
