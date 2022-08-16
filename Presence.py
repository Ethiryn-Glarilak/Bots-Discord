import argparse
import dotenv
import psutil
import random
import os
import pypresence
import time

if __name__ != "__main__":
    exit()

dotenv.load_dotenv()
client_id = os.getenv("client_id")  # Fake ID, put your real one here
RPC = pypresence.Presence(client_id,pipe=0)  # Initialize the client class
RPC.connect() # Start the handshake loop

parser = argparse.ArgumentParser("Presence.py")
parser.add_argument(
    "-q",
    "--quotes",
    dest = "option",
    type = str,
    help = "Get quotes type",
)
args = parser.parse_args()

quotes = {
    "philosophe" : [
        "If you can dream it, you can achieve it.",
        "Either write something worth reading or do something worth writing.",
        "You become what you believe.",
        "Fall seven times and stand up eight.",
        "The best revenge is massive success.",
        "Eighty percent of success is showing up.",
        "Life is what happens to you while you're busy making other plans.",
        "Strive not to be a success, but rather to be of value.",
        "The best time to plant a tree was 20 years ago. The second best time is now.",
        "Everything you've ever wanted is on the other side of fear.",
    ],  # The quotes to choose from
}.get(args.option, ["Error: No quotes found"])

counter = 60 * 60 * 4 + 60 * 30 + 50
increment = 5
while True:  # The presence will stay on as long as the program is running
    cpu_per = round(psutil.cpu_percent(),1) # Get CPU Usage
    mem = psutil.virtual_memory()
    mem_per = round(psutil.virtual_memory().percent,1)

    counter += increment

    RPC.update(
        state=random.choice(quotes),
        details=f"RAM: {str(mem_per)}% | CPU: {str(cpu_per)}%",
        start = time.time() - counter,
        large_image = "bot_icon",
        large_text = "My bot logo",
        small_image = "small_icon",
        small_text = "text of small_image",
        # party_size = [1, 4],
        buttons = [
            {
                "label": "-" + "Github".center(8) + "-",
                "url": "https://github.com/Ethiryn-Glarilak"
            },
            {
                "label": "-" + "Bots-Discord".center(14) + "-",
                "url": "https://github.com/Ethiryn-Glarilak/Bots-Discord"
            },
        ]
    )
    # counter -= 1

    time.sleep(increment) # Can only update rich presence every 15 seconds
