import random, pickle, glob

def elus(message):
    #Validator nom du fichier des elus
    if message.commande in ["0ec","0elus_choix"]:
        if not(message.user_id_int in [680605398549528613,694158393644023878]):
            fichiers = [dossier.split("-") for dossier in glob.glob("liste_elus/*")]
            continuer = False
            for fichier in fichiers:
                if fichier[0].split("\\")[-1].replace(".txt","") == message.parametre[1]:
                    continuer = True
        elif message.parametre[1] in ["0","TSI1"]:
            continuer = True
            message.parametre[1] = "TSI1_2019_2020"
        elif message.parametre[1] in ["1","gr5"]:
            continuer = True
            message.parametre[1] = "GROUPE_5"
        else:
            continuer = True
            message.parametre[1] = "TSI1_2019_2020"

    else:
        continuer = True
        if not(message.user_id_int in [680605398549528613,694158393644023878]):
            message.parametre = [message.parametre[0]] + ["TSI1_2019_2020"] + message.parametre[1:]
        elif message.parametre[1] in ["0","TSI1"]:
            message.parametre[1] = "TSI1_2019_2020"
        elif message.parametre[1] in ["1","gr5"]:
            message.parametre[1] = "GROUPE_5"

    if continuer == True:
        #Dictionnaire emojis et elus
        with open("Liste_Emojis.txt","r") as emojis_fichier:
            emojis_list = [":" + emojis + ":" for emojis in emojis_fichier.read().split("\n")]
        try:
            with open("liste_elus/" + message.parametre[1] + ".txt","r") as elus_fichier:
                elus_list = [elus.replace("?","'").split("_") for elus in elus_fichier.read().split("\n")]
        except:
            with open("TSI1_2019_2020.txt","r") as elus_fichier:
                elus_list = [elus.replace("?","'").split("_") for elus in elus_fichier.read().split("\n")]

        msg_elus_str = "Voici les élus pour cette heure :\n"

        #Gestion erreur sans commande sans argument et argument > nombre max de candidat
        try:
            nombre_elus = min(int(message.parametre[2]),len(elus_list))
        except:
            nombre_elus = 1

        #Génération des élus
        for elus_temp in range(nombre_elus):
            elus = random.choice(elus_list)
            emojis_str = random.choice(emojis_list)
            msg_elus_str += " - " + emojis_str + " " + elus[0] + "\n"
            elus_list.remove(elus)

        return msg_elus_str[:len(msg_elus_str)-1]
    else:
        return "Erreur lors de la saisie."