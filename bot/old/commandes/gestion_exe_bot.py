import discord

def fermer(message):
    msg = f"{message.auteur_str} ({message.nom_serveur}) [{message.nom_salon}] : {message}\nAction : mise hors ligne de {message.nom_bot} à {message.heure_c_str}"
    print(msg)
    return msg, discord.Embed(title="Action : ", description=f"Mise hors ligne de {message.nom_bot} à {message.heure_c_str}", colour=0xff0000)

def rouvrir(message):
    msg = f"{message.auteur_str} ({message.nom_serveur}) [{message.nom_salon}] : {message}\nAction : redémarrage de {message.nom_bot} à {message.heure_c_str}"
    print(msg)
    return msg, discord.Embed(title="Action : ", description=f"Redémarrage de Bot serveur à {message.heure_c_str}", colour=0x00ff00)