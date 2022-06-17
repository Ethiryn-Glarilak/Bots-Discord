import csv
import discord
import pathlib
import os
from src.data.postgres import DataBase
from extension.command_vjn.vjn_object import Status

async def get_data(message) -> None:
    bot = message.bot
    database : DataBase = bot.database.get("default")

    commandes = database.execute(f"SELECT id, id_user, quantity, status FROM command_VJN WHERE date >= '{os.getenv('date_data')}'").fetchall().value
    ingredient = database.execute("SELECT name FROM ingredient_VJN").fetchall()["name"]

    header = ["Nom"]
    header.extend(ingredient)

    tableau = []

    for commande in commandes:
        if commande[3] != Status.FINISH:
            continue;
        database.execute(f"SELECT id_ingredient FROM command_VJN JOIN product_ingredient_VJN ON command_VJN.id_product = product_ingredient_VJN.id_product WHERE command_VJN.id ={commande[0]}").fetchall()
        tableau.append([0] * (len(ingredient) + 1))
        tableau[-1][0] = str(bot.get_user(commande[1]))
        for product in database["id_ingredient"]:
            tableau[-1][product] = commande[2]

    event = pathlib.Path("data/guild/890357045138690108-VJN/event-list-produit/event-load").read_text()
    file = pathlib.Path(f"data/guild/890357045138690108-VJN/save/rapport-{event}.csv")

    with open(file, "w", encoding="utf-8") as f:
        write = csv.writer(f, lineterminator = "\n")
        write.writerow(header)
        write.writerows(tableau)


    if message.channel.type != discord.ChannelType.private or message.author.id == message.bot.user.id:
        await message.delete()
    await message.author.send(file = discord.File(file))
