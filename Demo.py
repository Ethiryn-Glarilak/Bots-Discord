import aiohttp
import src
import dotenv
import os

class Demo(src.Bot):

    def __init__(self) -> None:
        super().__init__("Démo", [0, 1], "D")
        self.log.get_logger(self.name).info("I start.")

if __name__ == "__main__":
    dotenv.load_dotenv()
    demo = Demo()
    try:
        demo.run(os.getenv("demo"))
    except aiohttp.ClientConnectionError:
        print("Failed to connect to demo")
