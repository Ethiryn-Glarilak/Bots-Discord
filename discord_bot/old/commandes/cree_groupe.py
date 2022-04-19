def cree_groupe(message):
    if not(message.parametre[1] in ["TSI1_2019_2020","GROUPE_5"]):
        #Validation nom du fichier d'enregistrement des emojis
        if message.parametre[1] == "0":
            message.parametre[1] = "TSI1_2019_2020"
        elif message.parametre[1].isnumeric():
            message.parametre[1] = "GROUPE_" + str(message.parametre[1])

        #Ouverture du fichier d'enregitrement des emojis
        try:
            with open("liste_elus/" + message.parametre[1] + ".txt","r") as elus_fichier:
                liste_elus = elus_fichier.read().split("\n")
        except:
            liste_elus = []

        #Ajouts des nouveaux élus à la liste des anciens
        elus_dict = {elus_temp:":" + elus_temp + ":" for elus_temp in (liste_elus + message.parametre[2:])}

        #Enregistrement des emojis dans le fichier
        with open("liste_elus/" + message.parametre[1] + ".txt","w") as elus_fichier:
            elus_fichier.write(str(list(elus_dict)).replace("[","").replace("]","").replace(",","").replace("'","").replace(" ","\n").replace("_"," "))

        return elus_dict
    else:
        return "Le groupe n'est pas modifiable"