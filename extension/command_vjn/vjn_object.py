import asyncio
from re import A
import discord
import enum
import json
import dotenv
import os
import pathlib

class Status(enum.IntEnum):
    COMMAND = 10
    PAYMENT_REQUIRED = 11
    PAYMENT_IN_PROGRESS = 12
    FILE_ATTENTE = 13
    PREPARATION_0 = 0
    PREPARATION_1 = 1
    PREPARATION_2 = 2
    PREPARATION_3 = 3
    PREPARATION_4 = 4
    PREPARATION_5 = 5
    PREPARATION_6 = 6
    PREPARATION_7 = 7
    PREPARATION_8 = 8
    PREPARATION_9 = 9
    READY = 14
    FINISH = 15

class VJNObject:

    def __init__(self, bot):
        # Raccourcis bot et database
        dotenv.load_dotenv(pathlib.Path(f"data/environment/.env{'' if bot.args.environment is None else f'-{bot.args.environment}'}"))
        self.database = bot.database.get("default")

        # Recuperation recette disponible
        event = pathlib.Path("data/guild/890357045138690108-VJN/event-list-produit/event-load").read_text()
        path_event = pathlib.Path(f"data/guild/890357045138690108-VJN/event-list-produit/{event}.json")
        if not path_event.exists():
            raise ValueError(f"Event file does not exist : {path_event}")
        with open(path_event, encoding="utf-8") as file:
            self.json = json.load(file)

        # Role Présent
        self.present = 987093379940753418
        self.present = 984575805663367188

    async def start(self, bot):
        # vjn = bot.get_guild(int(os.getenv("guild_VJN"))) # guild VJN
        # roles = list(map(lambda role : role.name, await vjn.fetch_roles()))

        # # FIXME NAME
        # if "Free" not in roles:
        #     bot.vjn_object.role_free = await vjn.create_role(name = "Free", colour = discord.Colour.blue())
        # else:
        #     bot.vjn_object.role_free = roles[roles.index("Free")]
        pass
