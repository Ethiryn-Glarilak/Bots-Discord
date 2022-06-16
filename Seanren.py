import aiohttp
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

    if platform.system() == "Windows":
        seanren.process = subprocess.Popen(["py", "-3", "Presence.py", "-q", seanren.args.quotes if seanren.args.quotes is not None else ""], shell = False)
        seanren.log.get_logger(seanren.name).info("Presence started")
    elif platform.system() == "Linux":
        seanren.process = subprocess.Popen(["python3", "Presence.py", "-q", seanren.args.quotes if seanren.args.quotes is not None else ""], shell = True)
        seanren.log.get_logger(seanren.name).info("Presence started")
    else:
        seanren.log.get_logger(seanren.name).error(f"os not supported : {platform.system()}")

    try:
        seanren.run(os.getenv("seanren"))
    except aiohttp.ClientConnectionError:
        print("Failed to connect to seanren")
    except Exception:
        print(Exception.args())
    finally:
        seanren.process.terminate()
        if process is not None:
            process.terminate()
