import bot
import dotenv
import os

class Ciaham(bot.Bot):

    def __init__(self) -> None:
        super().__init__("Ciaham", [3, 5], "C")
        self.log.get_logger(self.name).info("I start.")

if __name__ == "__main__":
    dotenv.load_dotenv()
    ciaham = Ciaham()
    ciaham.run(os.getenv("ciaham"))
