import os
from bot.old.class_object.messages_info import *
from bot.old.class_object.user_discord_coc import *

def associer(message):
    #Changement du dossier sources vers dossier compte coc
    dossier_travail = os.getcwd()
    os.chdir(os.path.join(dossier_travail,"compte_coc_membre"))

    #Donnees msg
    information = message_info(message,user_id_str = 0)

    #Récupération contenu fichier coc utilisateur
    liste_compte_coc = fichier_coc(information["user_id_str"])

    #Découpage données
    liste_compte_coc = [compte_coc.split(caractere_separation) for compte_coc in liste_compte_coc]

    #Validator nouvelle entré données


    #Création nouvelle entré msg utilisateur
    compte_coc = compte_coc(discord_ID = information["parametre"][1],
                            discord_nom_user = information["parametre"][2],
                            coc_ID = information["parametre"][3],
                            coc_nom_user = information["parametre"][4])

    #Ajout d'un nouvelle utilisateur
    compte_coc_dict = dict(liste_compte_coc + compte_coc)

    with open("compte_coc.txt","w") as fichier_compte_coc:
        fichier_compte_coc.write(str(compte_coc_dict).replace("{","").replace("}","").replace(",","").replace("'","").replace("_"," "))

    #Changement du dossier sources vers dossier serveur
    os.chdir(dossier_travail)

def recup_info(message):
    return messages_info(message,
                        user_name = "", user_id_int = 0, user_name_str = "", user_roles = "",
                        msg_date_created_int = 0, msg_date_created_str = "", serveur_str = "",
                        serveur_id_int = 0, serveur_id_str = "", salon_name_str = "",
                        user_id_str = "")

def fichier_coc(id_user):
    try:
        with open(f'{id_user}.txt', "r") as fichier_compte_coc:
            liste_compte_coc = fichier_compte_coc.read().split("\n")
    except Exception:
        liste_compte_coc = []
    return liste_compte_coc
