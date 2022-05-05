
def ajouter_emojis(message):
    #Validator nom du fichier d'enregistrement des emojis
    if 680605398549528613 != message.user_id_int:
        message.parametre = [message.parametre[0]] + ["Liste_Emojis"] + message.parametre[1:]
    elif message.parametre[1] == "0":
        message.parametre[1] = "Liste_Emojis"

    #Ouverture du fichier d'enregitrement des emojis
    try:
        with open(message.parametre[1] + ".txt","r") as emojis_fichier:
            emojis_list = emojis_fichier.read().split("\n")
    except:
        emojis_list = []

    #Ajouts des nouveaux emojis à la liste des anciens
    emojis_dict = {emojis:":" + emojis + ":" for emojis in(emojis_list + message.parametre[2:])}

    #Enregistrement des emojis dans le fichier
    with open(message.parametre[1] + ".txt","w") as emojis_fichier:
        emojis_fichier.write(str(list(emojis_dict)).replace("[","").replace("]","").replace(",","").replace("'","").replace(" ","\n"))

    #Renvoie la liste des emojis
    return emojis_dict