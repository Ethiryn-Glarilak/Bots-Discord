import random
#from modules.discord_bot.donnees.messages_info import *

def msg_discution(message):
    if message.commande in ["salut", "bonjour"]:
        return True, "Salut, moi ça vas et toi ?"
    if message.commande in ["super", "oui"]:
        return True, "Cool bonne journée sur le serveur !"
    if message.commande in ["merci", "sympa","de"]:
        return True, "Je t'en pris y a pas d'quoi."
    if message.commande in ["qui", "utilisateur"]:
        return True, "Tout le monde peux ce servir de ces commandes de discution."
    if message.commande in ["pas_de_soucis"]:
        return True, "Oulalalalalalalalalalalalala :stuck_out_tongue_winking_eye:."
    if message.commande in ["age", "naissance"]:
        return True, str(random.randint(0,2021)) + " ans"
    if "$" in message.commande or message.commande in ["maths"]:
        return True, "Tiens tu fais des maths"
    if message.commande in ["a"] and message.parametre[1] in ["demain", "plus"] and not(message.user_id_int in [694158393644023878]):
        with open("Liste_Emojis.txt","r") as emojis_fichier:
            emojis_list = [":" + emojis + ":" for emojis in emojis_fichier.read().split("\n")]
        emojis_str = random.choice(emojis_list)
        return True, str("A demain ! " + emojis_str)
    return False, ""