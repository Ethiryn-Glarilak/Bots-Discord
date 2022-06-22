import discord
import enum
import json
import dotenv
import os
import pathlib
from src.data.postgres import DataBase

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

        print("coucou")
        if os.getenv("ONLINE") is None:
            print("coucou1")
            self.database = bot.database.get("default")
        else:
            print("coucou2")
            if bot.args.test:
                print("coucou3")
                self.database = DataBase(bot, "postgres://impnxjpcbybilb:fb5a948a28f4d5356455cbb4f844f652ec279acb6384ccb3bb625040f9bf2b70@ec2-54-228-125-183.eu-west-1.compute.amazonaws.com:5432/dbiojci7uor6hp")
            else:
                print("coucou4")
                self.database = DataBase(
                    bot,
                    host = "ec2-54-228-125-183.eu-west-1.compute.amazonaws.com",
                    dbname = "de4cukfmv57pqs",
                    port = "5432",
                    user =  "snnppmggxxdubi",
                    password = "c56d6a1bfb097caca1d389f65cd3d2420187b3142e3ca7c0708c318b92a2a10a"
                )
            print("coucou5")
            bot.database["VJN"] = self.database
        print("coucou6")

        # Recuperation recette disponible
        event = pathlib.Path("data/guild/890357045138690108-VJN/event-list-produit/event-load").read_text()
        path_event = pathlib.Path(f"data/guild/890357045138690108-VJN/event-list-produit/{event}.json")
        if not path_event.exists():
            raise ValueError(f"Event file does not exist : {path_event}")
        with open(path_event, encoding="utf-8") as file:
            self.json = json.load(file)

        # Récupération id
        self.welcome = int(os.getenv("welcome"))
        self.command = int(os.getenv("command"))
        self.paiement = int(os.getenv("paiement"))
        self.assignment = int(os.getenv("assignment"))
        self.livraison = int(os.getenv("livraison"))
        self.log = int(os.getenv("log"))
        self.help = int(os.getenv("help"))
        self.roles = int(os.getenv("roles"))
        self.date_data = self.json.get("date_data")
        self.vjn = int(os.getenv("guild_VJN"))

    def check_role(self, name : str, roles : list[discord.Role]):
        return next((role for role in roles if role.name == name), None)

    async def start(self, bot):

        vjn : discord.Guild = bot.get_guild(self.vjn) # guild VJN
        roles = await vjn.fetch_roles()

        self.present = self.check_role("Présent", roles)
        if self.present is None:
            bot.log.get_logger(bot.name).error("Create Présent")
            self.present = await vjn.create_role(name = "Présent", colour = discord.Colour(0x1ABC9C))

        # FIXME NAME
        self.free = self.check_role("Free", roles)
        if self.free is None:
            self.free = await vjn.create_role(name = "Free", colour = discord.Colour.blue())

        print(f"Load {bot.name}")
