import aiohttp
import src
import dotenv
import os

class Ciaham(src.Bot):

    def __init__(self) -> None:
        super().__init__("Ciaham", [3, 5], "C")
        self.log.get_logger(self.name).info("I start.")

if __name__ == "__main__":
    dotenv.load_dotenv()
    ciaham = Ciaham()
    try:
        ciaham.run(os.getenv("ciaham"))
    except aiohttp.ClientConnectionError:
        print("Failed to connect to ciaham")
