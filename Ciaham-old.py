import discord, datetime, bot as mdb
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = "0")
cle = "NzA3ODg0MzIyNDY3ODcyNzc4.XrPTpg.YUwSfrwB9pvykiWcTKGeFGFqLAI"

nom = "Ciaham"
ver = "0.1.3"
lang = "fr"
print(f"{nom} {ver} {lang} lancé à {datetime.datetime.now()}")


@client.event
async def on_ready():
    change_status.start()
    print("Salut tout le monde !")

@client.event #Lancé quand un membre rejoint le serveur
async def on_member_join(membre):
    print(f"{membre} à rejoint le serveur à {membre.created_at}.")

@client.event #Lancé quand un membre quitte le serveur
async def on_member_remove(membre):
    print(f"{membre} à disparue du serveur à {membre.created_at}.")

@client.command(aliases = ["cr","nt","nettoyer"])
async def clear(context, nombre : int = 4):
    await context.channel.purge(limit = nombre + 1)
    print(f"{nombre} message(s) supprimé(s).")

@client.command()
async def fermer(context):
    # content, integration = mdb.fermer(mdb.message_info(context.message, nom = nom))
    # await context.channel.send(content, embed = integration)
    await client.close()


"""
@client.command(pass_context = True)
async def enlist(context, *, nickname):
    await client.change_nickname(context.message.author, nickname)
"""

status = cycle(["Apprend à s'autoprogrammer","Mange des crêpes avec Seanren"])
@tasks.loop(seconds = 10)
async def change_status():
    await client.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(next(status)))

"""
@client.event
async def on_message(message):
    #msg = mdb.message_info(message)
    author = message.author
    content = message.content
    print("{}: {}".format(author, content).replace("\n","_")

@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    await client.message.channel.send("{}: {}".format(author, content).replace("\n"," "))
"""
"""
@client.event
async def on_command_error(context, erreur):
    if isinstance(erreur, commands.MissingRequiredArgument):
        await context.send("S'il vous plait entré tout les arguments requis.")

@clear.error
async def clear_error(context, erreur):
    if isinstance(erreur, commands.MissingRequiredArgument):
        await context.send("S'il vous plait spécifier le nombre de messages à supprimer.")
"""

client.run(cle)