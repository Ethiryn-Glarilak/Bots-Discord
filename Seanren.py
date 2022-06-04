import bot
import dotenv
import os
import platform
import subprocess

class Seanren(bot.Bot):

    def __init__(self) -> None:
        super().__init__("Seanren", [3, 5], "S")
        self.log.get_logger(self.name).info("I start.")

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
