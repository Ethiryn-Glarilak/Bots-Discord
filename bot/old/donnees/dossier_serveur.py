import os, glob

def dossier_serveur(message,fichier):#Renvoie dirige vers le dossier de sauvegarde du serveur de provenance du message
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(fichier)).replace("\\Seanren",""),"donnees_serveurs"))
    dossiers = [dossier.split("-") for dossier in glob.glob("*")]
    for dossier in dossiers:
        if dossier[0] == message.id_serveur_str:
            os.chdir(os.path.join(os.getcwd(),dossier[0] + "-" + dossier[1]))